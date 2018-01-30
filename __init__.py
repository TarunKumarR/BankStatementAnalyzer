import pandas as pd
import glob
import os
import copy

'''
BankStatementAnalyzer --> To instantiate this class, following parameters are mandatory:
    statementfolder ---> Local file system folder where your bank statements are present. The folder can contain
                        multiple files. All the files should have same header and the first line of the file should be the header.
                        File can be of .csv or .txt or any plain text file extension.
    statementname --> A name for this Bank statement. Example values., creditcard, debit, savingaccount
    columnmap --> User needs to provide the following column mapping for the following 3 columns of your csv as these are the important
                    columns in a bank statement and it will be used to analyze the data.
                    Consider your Bank statement contains these 3 columns in header
                    Posted Date, Payee, Amount
                    then, you need to provide the following json as columnmap
                    {"Posted Date": "posted_date", "Payee": "payee",  "Amount": "amount"}
    dateformat --> This the format in which the posted_date column data will have data
    outputfolder --> This is the folder where the analyzed monthly splitup will be saved by the program. The user running the python script
                    should have access to this folder and the folder should have been already present.

'''
class BankStatementAnalyzer:
    def __init__(self, statementfolder,  statementname, columnmap, dateformat, outputfolder):
        self.statementfolder = statementfolder
        self.columnmap = columnmap
        self.outputfolder = outputfolder
        self.statementname = statementname
        self.dateformat = dateformat

    '''
    This function gets the list of files present on the folder provided by the user
    '''
    def __getfilelist(self, statementfolder):
        if os.path.isdir(statementfolder) is True:
            return [f for f in glob.glob(statementfolder + "*") if os.path.isfile(f) is True]
        else:
            raise "Path provided is not a folder or check if the path name is properly ended with a /"

    ''''
    This function gets the list of all files and creates a single dataframe consisting of data from all files.
    '''
    def __createdataframe(self):
        transdataframe = None
        filelist = self.__getfilelist(self.statementfolder)
        for ind, itm in enumerate(filelist):
            if ind is 0:
                transdataframe = pd.read_csv(itm, parse_dates = True, infer_datetime_format= True )
                transdataframe.rename(index=str, columns=self.columnmap, inplace=True)
            else:
                tempdataframe = pd.read_csv(itm)
                tempdataframe.rename(index=str, columns=self.columnmap, inplace=True)
                transdataframe = transdataframe.append(tempdataframe, ignore_index=True)

        transdataframe = transdataframe.assign(
            mon_year=(lambda x: pd.to_datetime(x.posted_date, format= self.dateformat).dt.year * 100 +
                                pd.to_datetime(x.posted_date, format= self.dateformat).dt.month))
        return transdataframe

    ''''
    This function splits the input data into months and stores it as csv files on the output folder
    '''
    def writeoutput(self):
        if os.path.isdir(self.outputfolder) is True:
            transdataframe = self.__createdataframe()
            for i in transdataframe.mon_year.unique():
                mon_year_mask = transdataframe['mon_year'].map(lambda x: x == i)
                ((transdataframe[mon_year_mask])[['posted_date','payee','amount']]).to_csv(self.outputfolder + str(i) + "_" + self.statementname + ".csv",index=False)
        else:
            raise "Path provided is not a folder or check if the path name is properly ended with a /"


    ''''
    This function returns all the transactions that have positive value
    '''
    def grouptransbyposval(self):
        transdataframe = self.__createdataframe()
        pos_amt_mask = transdataframe['amount'].map(lambda x: x > 0)
        posvaldataframe = (transdataframe[pos_amt_mask]).groupby(['mon_year'],
                                                       as_index=False)[["amount"]].sum()
        posvaldataframe.set_index("mon_year", inplace=True)
        return posvaldataframe

    ''''
    This function returns all the transactions that have negative value
    '''
    def grouptransbynegval(self):
        transdataframe = self.__createdataframe()
        neg_amt_mask = transdataframe['amount'].map(lambda x: x < 0)
        negvaldataframe = (transdataframe[neg_amt_mask]).groupby(['mon_year'], as_index=False)[["amount"]].sum()
        negvaldataframe.set_index("mon_year", inplace=True)
        return negvaldataframe

    ''''
    This function groups transcation by payee
    '''
    def grouptransbypayee(self):
        transdataframe = self.__createdataframe()
        payeegroupbydf = ((transdataframe).groupby(['payee', 'mon_year'], as_index=False)[["amount"]]).sum()
        return payeegroupbydf


    ''''
    This static function can merge 2 BankStatementAnalyzer objects
    '''
    @staticmethod
    def mergestatement(*statements):
        returnstatement = None
        for stmnt in statements:
            if returnstatement is None:
                returnstatement = copy.deepcopy(stmnt)
            else:
                returnstatement = returnstatement.add(stmnt, fill_value=0)
        return returnstatement


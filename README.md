# BankStatementAnalyzer
A python based bank statement analyzer which works using Pandas. The program will categorize transactions into monthly and also help in understanding how much is being saved each month.

## Overview
If you have problems in analyzing your monthly bank statment and not sure how much you saved each month, this program can help you solve that problem in following ways. 

* Once you have all your monthly/yearly bank statements ready in csv format, this program can help you tally the amounts across different accounts on monthly basis. 

* This also solves major problem in bank statements where previous months transcations will come into next month statement. This program will categorize and write transcations into csv files for each month.

## Prerequisites
This program requires pandas v0.22.0 or higher.


## Installing
pip install pandas

pip install BankStatementAnalyzer


## Demo
Consider that you have 3 bank accounts
* credit card account
* checking account
* saving account

you can do the following to easily check how much you saved on each month.

For this demo, the test data present in this location is used : [link](https://github.com/TarunKumarR/BankStatementAnalyzer/tree/master/testData)

1. Make sure you have all the bank statements in csv format stored in separate folder to each type of account.
        Example: Save all your credit card account statement to a folder called "credit". The folder can contain any number of csv files. Make sure all the files contain the same header.
2. To analyze all the credit card statements, following can be done.

```
from BankStatementAnalyzer import BankStatementAnalyzer
creditacct = BankStatementAnalyzer("testData/creditcard/", "credit", {"Posted Date": "posted_date",
        "Payee": "payee",  "Amount": "amount"},"%m/%d/%Y", "testoutput/") # here we instantiate the class BankStatementAnalyzer
print creditacct.grouptransbynegval() # using the grouptransbynegval method, you can get the sum of transactions having negative values
print creditacct.grouptransbyposval() # using the grouptransbyposval method, you can get the sum of transactions having positive values
print BankStatementAnalyzer.mergestatement(creditacct.grouptransbynegval(), creditacct.grouptransbyposval()) # to find the net amount of credit card statement on a monthly basis, merge the credit cards, positive and negative sums.

```
Similar to above, we can merge positive and negative sums from multiple statements to find the net amount we saved per month.

BankStatementAnalyzer --> To instantiate this class, following parameters are mandatory:
1. statementfolder ---> Local file system folder where your bank statements are present. The folder can contain multiple files. All the files should have same header and the first line of the file should be the header. File can be of .csv or .txt or any plain text file extension.
1. statementname --> A name for this Bank statement. Example values., creditcard, debit, savingaccount
1. columnmap --> User needs to provide the following column mapping for the following 3 columns of your csv as these are the important columns in a bank statement and it will be used to analyze the data.  Consider your Bank statement contains these 3 columns in header Posted Date, Payee, Amount then, you need to provide the following json as columnmap  {"Posted Date": "posted_date", "Payee": "payee",  "Amount": "amount"}  
1. dateformat --> This the format in which the posted_date column data will have data  
1. outputfolder --> This is the folder where the analyzed monthly splitup will be saved by the program. The user running the python script should have access to this folder and the folder should have been already present.


The BankStatementAnalyzer class needs the following parameters as input during it's instantiation.

BankStatementAnalyzer --> To instantiate this class, following parameters are mandatory:
1. statementfolder ---> Local file system folder where your bank statements are present. The folder can contain multiple files. All the files should have same header and the first line of the file should be the header. File can be of .csv or .txt or any plain text file extension.
1. statementname --> A name for this Bank statement. Example values., creditcard, debit, savingaccount
1. columnmap --> User needs to provide the following column mapping for the following 3 columns of your csv as these are the important columns in a bank statement and it will be used to analyze the data.  Consider your Bank statement contains these 3 columns in header Posted Date, Payee, Amount then, you need to provide the following json as columnmap  {"Posted Date": "posted_date", "Payee": "payee",  "Amount": "amount"}  
1. dateformat --> This the format in which the posted_date column data will have data  
1. outputfolder --> This is the folder where the analyzed monthly splitup will be saved by the program. The user running the python script should have access to this folder and the folder should have been already present.

Following code provides an example of getting transactions split into monthly basis and also on finding the net sum of amount saved across 3 accounts.
The input to the programs are present in folders "testData/creditcard/", "testData/saving/" and "testData/checking/".
The output of the following program is present in "testoutput/".

You can view the output of this test data in [link](https://github.com/TarunKumarR/BankStatementAnalyzer/tree/master/testoutput)

```
from BankStatementAnalyzer import BankStatementAnalyzer
creditacct = BankStatementAnalyzer("testData/creditcard/", "credit", {"Posted Date": "posted_date",
        "Payee": "payee",  "Amount": "amount"},"%m/%d/%Y", "testoutput/")
debitacct = BankStatementAnalyzer("testData/checking/", "debit", {"Date": "posted_date", "Description": "payee", "Amount": "amount",
                                           },"%m/%d/%Y", "testoutput/")
savingacct = BankStatementAnalyzer("testData/saving/", "saving", {"Date": "posted_date", "Description": "payee", "Amount": "amount",
                                           },"%m/%d/%Y", "testoutput/")

creditacct.writeoutput()
debitacct.writeoutput()
savingacct.writeoutput()
posNegSum = (BankStatementAnalyzer.mergestatement(creditacct.grouptransbynegval(), debitacct.grouptransbynegval(), savingacct.grouptransbynegval(),
                                                  creditacct.grouptransbyposval(), debitacct.grouptransbyposval(), savingacct.grouptransbyposval()))
posNegSum.to_csv("testoutput/monthlytally.csv")

```

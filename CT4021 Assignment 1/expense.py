import sqlite3
from sqlite3 import Error
import csv
#import pandas as pd
#use dataframe for 

#import numpy as np
#import pandas as pd
#import matploblib as mpl


# def create_connection(db_file):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#         global cur
#         cur = conn.cursor()
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()

# cur = None

conn = sqlite3.connect('expensesqlite.db')
c = conn.cursor()


options = {
    "1": " - set monthly income",
    "2": " - add new category",
    "3": " - list current categories",
    "4": " - set budget for categories",
    "5": " - enter expenses based on categories",
    "6": " - view expense report day/week/month",
    "7": " - print expense report to PDF",
    "8": " - view expense report by category",
    "9": " - print expense report to PDF",
    "o": " - See these options again",
    "e": " - Export to Excel",
    "q": " - Quit"
}


def printOptions():
    for key in options:
        val = options[key]
        print(key + val)


def handleOption(selectedOption):
    if selectedOption == "1":
        setMonthlyIncome()
    elif selectedOption == "2":
        addNewCategory()
    elif selectedOption == "3":
        listCategories()
    elif selectedOption == "4":
        setCategoryBudget()
    elif selectedOption == "5":
        setCategoryExpense()
    elif selectedOption == "6":
        showExpenseReportDWMY()
    elif selectedOption == "7":
        printPDFReportDWMY()
    elif selectedOption == "8":
        showExpenseByCategory()
    elif selectedOption == "9":
        printPDFReportByCategory()
    elif selectedOption == "e":
        exportExpensesToExcel()
    elif selectedOption == "o":
        printOptions()


def setMonthlyIncome():
    print(" setMonthlyIncome called")
    mIncome = input(int("Enter Monthly Income: £"))
    # test to see if income has been set already?
    # if it has been set ask the user to confirm if they want to overwrite it ?
    # or set it/reset it


def addNewCategory():
    print(" addNewCategory called")
    # get user input 
    inpCategory = input("Enter Category: ")
    c.execute("INSERT INTO categories ('name') VALUES ('" + inpCategory + "')")
    #inpBudget = input(int("Enter budget for category " + inpCategory + ": "))
    #c.execute("INSERT INTO categories ('budget') VALUES ('" + inpBudget + "')")
    conn.commit()
    conn.close()
    # and save to db
    print("Category: " + inpCategory + " has been saved with a budget of ")

def listCategories():
    print(" listCategories called")
    # get list from the database and print to screen - report to screen?
    # handle empty list from the db

def setCategoryBudget():
    print(" setCategoryBudget called")
    # get input from user of the catgeory and budget to set it against
    # update the db category using the category id to identify the category and update it's budget value

def setCategoryExpense():
    print(" setCategoryExpense called")
    # get input from user of the category and expense and date
    # save to the db

def showExpenseReportDWMY():
    print(" showExpenseReportDWMY called")
    # get input from user of the date
    # query db category expenses and output to the Report


def printPDFReportDWMY():
    print(" printPDFReportDWMY called")
    # get input from user of the date
    # query db category expenses and then print the list to a pdf using panda/matploblib ?


def showExpenseByCategory():
    print(" showExpenseByCategory called")
    # get input from user of specified category
    # query db for expenses in specified category

def printPDFReportByCategory():
    print(" printPDFReportByCategory called")
    # get input from user of specified category
    # query db category expenses and then print the list to a pdf using panda/matploblib ?

def exportExpensesToExcel():
    print(" exportExpensesToExcel called")
    # query db for all data to export to excel using pandas

################### start program ################################
# if __name__ == '__main__':
#     create_connection(
#         r"expensesqlite.db")


print("Welcome to your Expense Manager")
print("Please choose from the following options:")
printOptions()

while True:
    selectedOption = input("Select an option by its key: ")
    if selectedOption == "q":
        break
    handleOption(selectedOption)
##################################################################

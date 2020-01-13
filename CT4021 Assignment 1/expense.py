import sqlite3
from sqlite3 import Error
import csv
import sys
from colorama import Fore
from colorama import Style
from colorama import AnsiToWin32
import pandas as pd
from pandas import DataFrame as df
#import locale
#from openpyxl.workbook import Workbook
import xlsxwriter

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

conn = sqlite3.connect('expensesqlite.db')
c = conn.cursor()

######################### print data ############################

options = {
    "1": " - Manage Income",
    "2": " - Manage Expense Categories",
    "3": " - Manage Expenses",
    "4": " - Report Options",
    "e": " - Export to Excel",
    "o": " - See these options again",
    "q": " - Quit\n"
}

incomeOptions = {
    "\nManage Incomes\n"
        "1": " - Set monthly income",
        "2": " - Update current incomes",
        "3": " - Delete  incomes",
        "b": " - Back\n"
    }

categoryOptions = {
    "\nManage Expense Categories\n"
        "1": " - Add new category",
        "2": " - Update current categories",
        "3": " - Delete categories",
        "4": " - Set or update budget for categories",
        "b": " - Back\n"
}

expenseOptions = {
    "\nManage Expenses\n"
        "1": " - Add new expense",
        "2": " - Update current expenses",
        "3": " - Delete expenses",
        "b": " - Back\n"
}

reportOptions = {
    "\nReport Options\n"
        "1": " - View expense report day/week/month",
        "2": " - View expense report graph",
        "3": " - Print expense report to PDF by date",
        "4": " - Print expense report to PDF by category",
        "b": " - Back\n"
}

##################################################################

####################### print options ############################

def printOptions():
    for key in options:
        val = options[key]
        print(key + val)
    selectedOption=input("Select an option by its key: ")
    handleOption(selectedOption)
    if selectedOption == "q":
        conn.close()
        sys.exit(0)
        
def printIncomeOptions():
    for key in incomeOptions:
        val = incomeOptions[key]
        print(key + val)
    selectedIncOption=input("Select an option by its key: ")
    handleOptionIncome(selectedIncOption)
    if selectedIncOption == "q":
        conn.close()
        sys.exit(0)


def printCategoryOptions():
    for key in categoryOptions:
        val = categoryOptions[key]
        print(key + val)
    selectedCatOption=input("Select an option by its key: ")
    handleOptionCategory(selectedCatOption)
    if selectedCatOption == "q":
        conn.close()
        sys.exit(0)

def printExpenseOptions():
    for key in expenseOptions:
        val = expenseOptions[key]
        print(key + val)
    selectedExpOption=input("Select an option by its key: ")
    handleOptionExpense(selectedExpOption)
    if selectedExpOption == "q":
        conn.close()
        sys.exit(0)

def printReportOptions():
    for key in reportOptions:
        val = reportOptions[key]
        print(key + val)
    selectedRepOption=input("Select an option by its key: ")
    handleOptionReport(selectedRepOption)
    if selectedRepOption == "q":
        conn.close()
        sys.exit(0)

##################################################################

###################### handle options ############################

# Decide which menu is called based on user input
def handleOption(selectedOption):
    if selectedOption == "1":
        printIncomeOptions()
    elif selectedOption == "2":
        printCategoryOptions()
    elif selectedOption == "3":
        printExpenseOptions()
    elif selectedOption == "4":
        printReportOptions()
    elif selectedOption == "e":
        exportExpensesToExcel()
    elif selectedOption == "o":
        printOptions()
    
# Decide which function is called for incomes menu 
def handleOptionIncome(selectedIncOption):
    if selectedIncOption == "1":
        setMonthlyIncome()
    elif selectedIncOption == "2":
        updateMonthlyIncome()
    elif selectedIncOption == "3":
        deleteMonthlyIncome()
    elif selectedIncOption == "b":
        printOptions()

# Decide which function is called for categories menu 
def handleOptionCategory(selectedCatOption):
    if selectedCatOption == "1":
        addNewCategory()
    elif selectedCatOption == "2":
        updateCategories()
    elif selectedCatOption == "3":
        deleteCategories()
    elif selectedCatOption == "4":
        setCategoryBudget()
    elif selectedCatOption == "b":
        printOptions()  

# Decide which function is called for expenses menu 
def handleOptionExpense(selectedExpOption):
    if selectedExpOption == "1":
        addCategoryExpense()
    elif selectedExpOption == "2":
        updateExpense()
    elif selectedExpOption == "3":
        deleteExpense()
    elif selectedExpOption == "b":
        printOptions()  
  
# Decide which function is called for reports menu   
def handleOptionReport(selectedRepOption):
    if selectedRepOption == "1":
        showExpenseReportDWMY()
    elif selectedRepOption == "2":
        graphExpense()
    elif selectedRepOption == "3":
        printPDFReportDWMY()
    elif selectedRepOption == "4":
        printPDFReportByCategory()
    elif selectedRepOption == "b":
        printOptions()  
    

##################################################################

###################### income functions ##########################

def tableIncome():
    table = pd.read_sql_query("SELECT * FROM mIncome", conn)
    print(table)
    conn.commit()

def setMonthlyIncome():
    print(" setMonthlyIncome called\n")
    inpSource = input("Enter income source: ")
    inpIncome = input("Enter monthly income: £")
    c.execute("INSERT INTO mIncome (source) VALUES ('" + inpSource + "')")
    c.execute("UPDATE mIncome SET (income) = ('" + inpIncome + "') WHERE source = ('" + inpSource + "')")
    incomeTotal = c.execute("SELECT source,SUM(income) FROM mIncome as total")
    #c.execute("INSERT INTO mIncome (income) VALUES ('" + incomeTotal + "')")
    print(incomeTotal)
    conn.commit()
    print("Source of income has been saved")
    inpMult = input("To add another source of income, enter 'y',\n otherwise press keyboard: ")
    if inpMult == ('y' or 'Y'):
        setMonthlyIncome()
    else:
        printOptions()
    # test to see if income has been set already?
    # if it has been set ask the user to confirm if they want to overwrite it ?
    # or set it/reset it


def updateMonthlyIncome():
    print(" updateMonthlyIncome called\n")
    tableIncome()
    inpSource = input("\nEnter income source to update: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM mIncome WHERE source=? LIMIT 1)", (inpSource,))
    record=c.fetchone()
    if record[0] == 1:
        inpIncome = input("Enter a new income: £")
        c.execute("UPDATE mIncome SET (income) = (" + inpIncome + ") WHERE source = ('" + inpSource + "')")
        conn.commit()
        print("Income has been updated")
    else:
        print("Source does not exist, please try again\n")
        updateMonthlyIncome()


def deleteMonthlyIncome():
    print(" deleteMonthlyIncome called\n")
    tableIncome()
    inpSource = input("\nEnter income source to delete: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpSource,))
    record=c.fetchone()
    if record[0] == 1:
        c.execute("DELETE FROM mIncome WHERE name = ('" + inpSource + "')")
        conn.commit()
        print("Income source has been deleted")
    else:
        print("Source does not exist, please try again\n")
        deleteMonthlyIncome()

###################### category functions ##########################

def tableCategory():
    table = pd.read_sql_query("SELECT * FROM categories", conn)
    print(table)
    conn.commit()


def addNewCategory():
    print(" addNewCategory called\n")
    # get user input
    inpCategory = input("Enter new category: ")
    # and save to db category table
    c.execute("INSERT INTO categories (name) VALUES ('" + inpCategory + "')")
    conn.commit()
    print("Category '" + inpCategory + "' has been saved")


def updateCategories():
    print(" updateCategories called\n")
    tableCategory()
    inpCategory = input("\nEnter category to update: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,))
    record=c.fetchone()
    if record[0] == 1:
        inpNewCategory = input("Enter new category name: ")
        c.execute("UPDATE categories SET (name) = ('" + inpNewCategory + "') WHERE name = ('" + inpCategory + "')")
        conn.commit()
        print("Category has been updated")
    else:
        print("Category does not exist, please try again\n")
        printOptions()


def deleteCategories():
    print(" deleteCategories called\n")
    tableCategory()
    inpCategory = input("\nEnter category to delete: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,))
    record=c.fetchone()
    if record[0] == 1:
        c.execute("DELETE FROM categories WHERE name = ('" + inpCategory + "')")
        conn.commit()
        print("Category has been deleted")
    else:
        print("Category does not exist, please try again\n")
        deleteCategories()


# get input from user of the catgeory and budget to set it against
def setCategoryBudget():
    print(" setCategoryBudget called\n")
    tableCategory()
    inpCategory = input("\nEnter category to add a budget to: ")
    checkCatExists()
    if record[0] == 1:
        inpBudget = input("Enter a budget: £")
        c.execute("UPDATE categories SET (budget) = ('" + inpBudget + "') WHERE name = ('" + inpCategory + "')")
        conn.commit()
        print("budget has been saved")
    else:
        print("Category does not exist, please enter a valid category\n")
        setCategoryBudget()
    

###################### expense functions ##########################
def tableExpense():
    table = pd.read_sql_query("SELECT * FROM expenses", conn)
    print(table)
    conn.commit()

def checkExpExists():
    c.execute("SELECT EXISTS(SELECT 1 FROM expenses WHERE name=? LIMIT 1)", (inpExpense,))
    record=c.fetchone()

    

def addCategoryExpense():
    print(" addCategoryExpense called\n")
    inpName=input("Enter expense name: ")
    tableCategory()
    inpCategory=input("\nEnter category to add expense to: ")
    inpCost=input("Enter expense cost: ")
    inpDate=input("Enter expense date(YYYY-MM-DD): ")
    checkCatExists()
    if record[0] == 1:
        c.execute("INSERT INTO expenses (name, category, cost, date) VALUES ('" + inpName + "', '" + inpCategory + "', '" + inpCost + "', '" + inpDate + "')")
        avgCost = c.execute("SELECT 1 FROM expenses WHERE cost=('" + inpCost + "') LIMIT 1")
        avgBudget = c.execute("SELECT (budget) FROM categories WHERE name=('" + inpCategory + "') LIMIT 1")
        avgExpense = (avgBudget - avgCost)
        conn.commit()
        print("New expense has been saved")
    else:
        print("Category does not exist, please try again or add new category\n")
        addCategoryExpense()
    # get input from user of the category and expense and date
    # save to the db

def updateExpense():
    print(" updateExpense called\n")
    tableExpense()
    inpExpense = input("\nEnter expense to update: ")
    checkExpExists()
    if record[0] == 1:
        inpNewExpense = input("Enter new expense value: ")
        c.execute("UPDATE expenses SET (name) = ('" + inpNewExpense + "') WHERE name = ('" + inpExpense + "')")
        conn.commit()
        print("Expense has been updated")
    else:
        print("Expense does not exist, please try again or add new expense\n")
        updateExpense()


def deleteExpense():
    print(" updateExpense called\n")
    tableExpense()
    inpExpense = input("\nEnter expense to delete: ")
    checkExpExists()
    if record[0] == 1:
        c.execute("DELETE FROM expenses WHERE name = ('" + inpExpense + "')")
        conn.commit()
        print("Expense has been deleted")
    else:
        print("Expense does not exist, please try again\n")
        deleteExpense()


###################### report functions ##########################

def showExpenseReportDWMY():
    print(" showExpenseReportDWMY called\n")
    # get input from user of the date
    # query db category expenses and output to the Report


def graphExpense():
    print(" showExpenseByCategory called\n")
    dfTableExp = pd.read_sql_query("SELECT * FROM expenses", conn)
    #plt.hist(dfTableExp.name,dfTableExp.cost,histtype='bar',rwidth=0.8)
    dfTableExp.plot(kind='bar',x='name',y='cost',color='red')
    plt.title("Expense Graph")
    plt.ylabel("Cost (£)")
    plt.xlabel("Expense")
    plt.legend()
    plt.show()
    conn.commit()
    # get input from user of specified category
    # query db for expenses in specified category
    

    def printPDFReportDWMY():
    print(" printPDFReportDWMY called\n")
    # get input from user of the date
    # query db category expenses and then print the list to a pdf using panda/matploblib ?


def printPDFReportByCategory():
    print(" printPDFReportByCategory called\n")
    
    # get input from user of specified category
    # query db category expenses and then print the list to a pdf using panda/matploblib ?


def exportExpensesToExcel():
    print(" exportExpensesToExcel called\n")
    dfTableInc = pd.read_sql_query("SELECT * FROM mIncome", conn)
    dfTableCat = pd.read_sql_query("SELECT * FROM categories", conn)
    dfTableExp = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.commit()
    
    writer = pd.ExcelWriter('expenseSheet.xlsx',engine='xlsxwriter')   
    workbook=writer.book
    worksheet=workbook.add_worksheet('Expense Data')
    writer.sheets['Expense Data'] = worksheet
    dfTableInc.to_excel(writer,sheet_name='Expense Data',startrow=0 , startcol=0)   
    dfTableCat.to_excel(writer,sheet_name='Expense Data',startrow=0, startcol=5)
    dfTableExp.to_excel(writer,sheet_name='Expense Data',startrow=0, startcol=10)
    workbook.close()

    print("Data with 3 tables exported successfully")

##################################################################

################### start program ################################

print("Welcome to your Expense Manager")
print("Please choose from the following options:\n")
printOptions()

##################################################################

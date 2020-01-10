import sqlite3
from sqlite3 import Error
import csv
import pandas as pd
from pandas import DataFrame as df
# use dataframe for excel
#import locale

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
    "q": " - Quit from any menu\n"
}

incomeOptions = {
    "Manage Incomes\n"
        "1": " - Set monthly income",
        "2": " - Update current incomes",
        "3": " - Delete  incomes",
        "b": " - Back\n"
    }

categoryOptions = {
    "Manage Expense Categories\n"
        "1": " - Add new category",
        "2": " - Update current categories",
        "3": " - Delete categories",
        "4": " - Set or update budget for categories",
        "b": " - Back\n"
}

expenseOptions = {
    "Manage Expenses\n"
        "1": " - Add new expense",
        "2": " - Update current expenses",
        "3": " - Delete expenses",
        "b": " - Back\n"
}

reportOptions = {
    "Report Options\n"
        "1": " - View expense report day/week/month",
        "2": " - View expense report by category",
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

def printIncomeOptions():
    for key in incomeOptions:
        val = incomeOptions[key]
        print(key + val)
    selectedIncOption=input("Select an option by its key: ")
    handleOptionIncome(selectedIncOption)

def printCategoryOptions():
    for key in categoryOptions:
        val = categoryOptions[key]
        print(key + val)
    selectedCatOption=input("Select an option by its key: ")
    handleOptionCategory(selectedCatOption)

def printExpenseOptions():
    for key in expenseOptions:
        val = expenseOptions[key]
        print(key + val)
    selectedExpOption=input("Select an option by its key: ")
    handleOptionExpense(selectedExpOption)

def printReportOptions():
    for key in reportOptions:
        val = reportOptions[key]
        print(key + val)
    selectedRepOption=input("Select an option by its key: ")
    handleOptionReport(selectedRepOption)

##################################################################

###################### handle options ############################

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
    elif selectedOption == "q":
        conn.close()
        quit
        
    
def handleOptionIncome(selectedIncOption):
    #incomes
    if selectedIncOption == "1":
        setMonthlyIncome()
    elif selectedIncOption == "2":
        updateMonthlyIncome()
    elif selectedIncOption == "3":
        deleteMonthlyIncome()
    elif selectedIncOption == "b":
        printOptions()

def handleOptionCategory(selectedCatOption):
    #categories
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

def handleOptionExpense(selectedExpOption):
    #expenses
    if selectedExpOption == "1":
        addCategoryExpense()
    elif selectedExpOption == "2":
        updateExpense()
    elif selectedExpOption == "3":
        deleteExpense()
    elif selectedExpOption == "b":
        printOptions()  

def handleOptionReport(selectedRepOption):
    #reports  
    if selectedRepOption == "1":
        showExpenseReportDWMY()
    elif selectedRepOption == "2":
        showExpenseByCategory()
    elif selectedRepOption == "3":
        printPDFReportDWMY()
    elif selectedRepOption == "4":
        printPDFReportByCategory()
    elif selectedRepOption == "b":
        printOptions()  
    

##################################################################

###################### main functions ############################

def setMonthlyIncome():
    print(" setMonthlyIncome called\n")
    inpSource = input("Enter income source: ")
    inpIncome = input("Enter monthly income: £")
    c.execute("INSERT INTO mIncome (source) VALUES ('" + inpSource + "')")
    c.execute("UPDATE mIncome SET (income) = ('" + inpIncome + "') WHERE source = ('" + inpSource + "')")
    incomeTotal = c.execute("SELECT * FROM mIncome (income)")
    print(incomeTotal)
    conn.commit()
    print("Source of income has been saved")
    inpMult = input("To add another source of income, enter 'y', \notherwise press keyboard: ")
    if inpMult == ('y' or 'Y'):
        setMonthlyIncome()
    else:
        printOptions()
    # test to see if income has been set already?
    # if it has been set ask the user to confirm if they want to overwrite it ?
    # or set it/reset it


def updateMonthlyIncome():
    print(" updateMonthlyIncome called\n")
    table = pd.read_sql_query("SELECT * FROM mIncome", conn)
    print(table)
    conn.commit()
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
    print("  called\n")


def addNewCategory():
    print(" addNewCategory called\n")
    # get user input
    inpCategory = input("Enter new category: ")
    # and save to db
    c.execute("INSERT INTO categories (name) VALUES ('" + inpCategory + "')")
    conn.commit()
    print("Category '" + inpCategory + "' has been saved")


def updateCategories():
    print(" updateCategories called\n")
    table = pd.read_sql_query("SELECT * FROM categories", conn)
    print(table)
    conn.commit()
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
        updateCategories()


def deleteCategories():
    print("  called\n")


def setCategoryBudget():
    print(" setCategoryBudget called\n")
    table = pd.read_sql_query("SELECT * FROM categories", conn)
    print(table)
    conn.commit()
    inpCat = input("\nEnter category to add a budget to: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCat,))
    record=c.fetchone()
    if record[0] == 1:
        inpBudget = input("Enter a budget: £")
        c.execute("UPDATE categories SET (budget) = ('" + inpBudget + "') WHERE name = ('" + inpCat + "')")
        conn.commit()
        print("budget has been saved")
    else:
        print("Category does not exist, please enter a valid category\n")
        setCategoryBudget()
    
    # get input from user of the catgeory and budget to set it against
    # update the db category using the category id to identify the category and update it's budget value


def addCategoryExpense():
    print(" addCategoryExpense called\n")
    inpName=input("Enter Expense Name: ")
    inpCat=input("Enter Expense Category: ")
    inpCost=input("Enter Expense Cost: ")
    inpDate=input("Enter Expense Date(YYYY-MM-DD): ")
    c.execute("INSERT INTO expenses (name, category, cost, date) VALUES ('" + \
              inpName + "', '" + inpCat + "', '" + inpCost + "', '" + inpDate + "')")
    conn.commit()
    # conn.close()
    print("New expense has been saved")
    # get input from user of the category and expense and date
    # save to the db

def updateExpense():
    print(" updateExpense called\n")
    table = pd.read_sql_query("SELECT * FROM expenses", conn)
    print(table)
    conn.commit()
    inpExpense = input("\nEnter expense to update: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM expenses WHERE name=? LIMIT 1)", (inpExpense,))
    record=c.fetchone()
    if record[0] == 1:
        inpNewExpense = input("Enter new expense value: ")
        c.execute("UPDATE expenses SET (name) = ('" + inpNewExpense + "') WHERE name = ('" + inpExpense + "')")
        conn.commit()
        print("Expense has been updated")
    else:
        print("Expense does not exist, please try again\n")
        updateCategories()


def deleteExpense():
    print("  called\n")


def showExpenseReportDWMY():
    print(" showExpenseReportDWMY called\n")
    # get input from user of the date
    # query db category expenses and output to the Report


def printPDFReportDWMY():
    print(" printPDFReportDWMY called\n")
    # get input from user of the date
    # query db category expenses and then print the list to a pdf using panda/matploblib ?


def showExpenseByCategory():
    print(" showExpenseByCategory called\n")
    inpExpenseCat=input("Enter category to view expense of: ")
    c.execute("SELECT * FROM expenses WHERE category = ('" + inpExpenseCat + "')")
    result=c.fetchall()
    for result in result:
        print(result)
    conn.commit()
    # get input from user of specified category
    # query db for expenses in specified category

def printPDFReportByCategory():
    print(" printPDFReportByCategory called\n")
    # get input from user of specified category
    # query db category expenses and then print the list to a pdf using panda/matploblib ?

def exportExpensesToExcel():
    print(" exportExpensesToExcel called\n")
    # df.to_excel(r'Path where you want to store the exported excel file\File Name.xlsx')
    # query db for all data to export to excel using pandas

##################################################################

################### start program ################################

print("Welcome to your Expense Manager")
print("Please choose from the following options:\n")
printOptions()

##################################################################

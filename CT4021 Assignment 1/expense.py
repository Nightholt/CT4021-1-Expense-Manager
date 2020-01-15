import sqlite3
from sqlite3 import Error
import sys
import pdfkit as pdf
import xlsxwriter

import pandas as pd
from pandas import DataFrame as df
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

conn = sqlite3.connect('expensesqlite.db')
c = conn.cursor()

######################### print data ############################
#navigation of program
# dictionary for main options, called by printOptions
options = {
    "Main Menu\n"
    "1": " - Manage Income",
    "2": " - Manage Expense Categories",
    "3": " - Manage Expenses",
    "4": " - Report Options",
    "e": " - Export to Excel",
    "o": " - See these options again",
    "q": " - Quit\n"
}

# dictionary for income options, called by printIncomeOptions
incomeOptions = {
    "\nManage Incomes\n"
    "1": " - Set monthly income",
    "2": " - Update current incomes",
    "3": " - Delete  incomes",
    "b": " - Back\n"
}

# dictionary for category options, called by printCategoryOptions
categoryOptions = {
    "\nManage Expense Categories\n"
    "1": " - Add new category",
    "2": " - Update current categories",
    "3": " - Delete categories",
    "4": " - Set or update budget for categories",
    "b": " - Back\n"
}

# dictionary for expense options, called by printExpenseOptions
expenseOptions = {
    "\nManage Expenses\n"
    "1": " - Add new expense",
    "2": " - Update current expenses",
    "3": " - Delete expenses",
    "b": " - Back\n"
}

# dictionary for report options, called by printReportOptions
reportOptions = {
    "\nReport Options\n"
    "1": " - Print all expenses report to pdf",
    "2": " - Print expense report to PDF by date",
    "3": " - Print expense report to PDF by category",
    "4": " - Print over/under report to PDF",
    "b": " - Back\n"
}

# dictionary for report by date options, called by printReportbyDWMY
reportDateOptions = {
    "\nExpense Report by Date Options\n"
    "1": " - View expense report by range (year/month)",
    "2": " - View expense report by day",
    "b": " - Back\n"
}

##################################################################

####################### print options ############################
# loops called from functions to navigate the program and exit 
#main menu
def printOptions():
    for key in options:
        val = options[key]
        print(key + val)
    selectedOption = input("Select an option by its key: ")
    handleOption(selectedOption)
    if selectedOption == "q": #close db and quit program
        conn.close() 
        sys.exit(0)

#income menu
def printIncomeOptions():
    for key in incomeOptions:
        val = incomeOptions[key]
        print(key + val)
    selectedIncOption = input("Select an option by its key: ")
    handleOptionIncome(selectedIncOption)
    if selectedIncOption == "q":
        conn.close()
        sys.exit(0)

#category menu
def printCategoryOptions():
    for key in categoryOptions:
        val = categoryOptions[key]
        print(key + val)
    selectedCatOption = input("Select an option by its key: ")
    handleOptionCategory(selectedCatOption)
    if selectedCatOption == "q":
        conn.close()
        sys.exit(0)

#expense menu
def printExpenseOptions():
    for key in expenseOptions:
        val = expenseOptions[key]
        print(key + val)
    selectedExpOption = input("Select an option by its key: ")
    handleOptionExpense(selectedExpOption)
    if selectedExpOption == "q":
        conn.close()
        sys.exit(0)

#report menu
def printReportOptions():
    for key in reportOptions:
        val = reportOptions[key]
        print(key + val)
    selectedRepOption = input("Select an option by its key: ")
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
        graphExpense()
    elif selectedRepOption == "2":
        printPDFReportDWMY()
    elif selectedRepOption == "3":
        printPDFReportByCategory()
    elif selectedRepOption == "4":
        avgOverUnder()
    elif selectedRepOption == "b":
        printOptions()


##################################################################

###################### income functions ##########################

def tableIncome():
    table = pd.read_sql_query("SELECT * FROM mIncome", conn)
    print(table)
    conn.commit()

def updateTotal():
    incomeTotal = pd.read_sql_query("SELECT SUM(income) FROM mIncome", conn)
    c.execute("UPDATE mIncome SET (total) = ('" + str(incomeTotal.iloc[0,0]) + "')")

def setMonthlyIncome():
    print(" setMonthlyIncome called\n")
    inpSource = input("Enter income source: ")
    inpIncome = input("Enter monthly income: £")
    c.execute("INSERT INTO mIncome (source) VALUES ('" + inpSource + "')")
    c.execute("UPDATE mIncome SET (income) = ('" + inpIncome +"') WHERE source = ('" + inpSource + "')")
    updateTotal()
    conn.commit()
    print("Income has been saved\n")
    printOptions()
   

def updateMonthlyIncome():
    print(" updateMonthlyIncome called\n")
    tableIncome()
    inpSource = input("\nEnter income source to update: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM mIncome WHERE source=? LIMIT 1)", (inpSource,))
    record = c.fetchone()
    if record[0] == 1:
        inpIncome = input("Enter a new income: £")
        c.execute("UPDATE mIncome SET (income) = (" + inpIncome +") WHERE source = ('" + inpSource + "')")
        updateTotal()
        print("Income has been updated\n")
        printOptions()
    else:
        print("Source does not exist, please try again or add new source\n")
        printIncomeOptions()


def deleteMonthlyIncome():
    print(" deleteMonthlyIncome called\n")
    tableIncome()
    inpSource = input("\nEnter income source to delete by mid: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM mIncome WHERE mid=? LIMIT 1)", (inpSource,))
    record = c.fetchone()
    if record[0] == 1:
        c.execute("DELETE FROM mIncome WHERE mid = ('" + inpSource + "')")
        updateTotal()
        conn.commit()
        print("Income source has been deleted\n")
        printOptions()
    else:
        print("Source does not exist, please try again or add new source\n")
        printIncomeOptions()

###################### category functions ##########################


def tableCategory():
    table = pd.read_sql_query("SELECT (name) FROM categories", conn)
    print(table)
    conn.commit()


def addNewCategory():
    print(" addNewCategory called\n")
    # get user input
    inpCategory = input("Enter new category: ")
    # and save to db category table
    c.execute("INSERT INTO categories (name) VALUES ('" + inpCategory + "')")
    conn.commit()
    print("New category has been saved\n")
    printOptions()


def updateCategories():
    print(" updateCategories called\n")
    tableCategory()
    inpCategory = input("\nEnter category to update: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,))
    record = c.fetchone()
    if record[0] == 1:
        inpNewCategory = input("Enter new category name: ")
        c.execute("UPDATE categories SET (name) = ('" +
                  inpNewCategory + "') WHERE name = ('" + inpCategory + "')")
        conn.commit()
        print("Category has been updated\n")
        printOptions()
    else:
        print("Category does not exist, please try again\n")
        printCategoryOptions()


def deleteCategories():
    print(" deleteCategories called\n")
    tableCategory()
    inpCategory = input("\nEnter category to delete: ")
    c.execute(
        "SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,))
    record = c.fetchone()
    if record[0] == 1:
        c.execute("DELETE FROM categories WHERE name = ('" + inpCategory + "')")
        conn.commit()
        print("Category has been deleted\n")
        printOptions()
    else:
        print("Category does not exist, please try again\n")
        printCategoryOptions()


# get input from user of the catgeory and budget to set it against
def setCategoryBudget():
    print(" setCategoryBudget called\n")
    tableCategory()
    inpCategory = input("\nEnter category to add a budget to: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,))
    if record[0] == 1:
        inpBudget = input("Enter a budget: £")
        c.execute("UPDATE categories SET (budget) = ('" + inpBudget + "') WHERE name = ('" + inpCategory + "')")
        conn.commit()
        print("budget has been saved\n")
        printOptions()
    else:
        print("Category does not exist, please enter a valid category\n")
        printCategoryOptions()


###################### expense functions ##########################

# func to print expenses for user to select from that looks nice
def tableExpense():
    table = pd.read_sql_query("SELECT * FROM expenses", conn) # creates dataframe from db selection
    print(table)
    conn.commit()


def addCategoryExpense():
    print(" addCategoryExpense called\n")
    inpExpense = input("Enter expense name: ")
    tableCategory()
    inpCategory = input("\nEnter category to add expense to: ")
    inpCost = input("Enter expense cost: ")
    inpDate = input("Enter expense date(YYYY-MM-DD): ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,))
    record = c.fetchone()
    if record[0] == 1:
        c.execute("INSERT INTO expenses (name, category, cost, date) VALUES ('" + inpExpense + "', '" + inpCategory + "', '" + inpCost + "', '" + inpDate + "')")
        avgCost = pd.read_sql_query("SELECT (cost) FROM expenses WHERE name=('" + inpExpense + "')", conn)
        totCost = pd.read_sql_query("SELECT SUM(cost) FROM expenses WHERE category=('"+ inpCategory +"')", conn)
        avgBudget = pd.read_sql_query("SELECT (budget) FROM categories WHERE name=('" + inpCategory + "') LIMIT 1", conn)
        avgExpense = (avgBudget.iloc[0,0] - avgCost.iloc[0,0])
        totExpense = (avgBudget.iloc[0,0] - totCost.iloc[0,0])
        c.execute("UPDATE expenses SET (overUnder) = ('"+ str(round(avgExpense, 2)) +"') WHERE name=('"+ inpExpense +"')")
        c.execute("UPDATE expenses SET (catTotal) = ('"+ str(round(totExpense, 2)) +"') WHERE category=('"+ inpCategory +"')")
        conn.commit()
        print("New expense has been saved\n")
        printOptions()
    else:
        print("Category does not exist, please try again or add new category\n")
        printExpenseOptions()
    # get input from user of the category and expense and date
    # save to the db


def updateExpense():
    print(" updateExpense called\n")
    tableExpense()
    inpExpense = input("\nEnter expense to update by eid: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM expenses WHERE eid=? LIMIT 1)", (inpExpense,))
    record = c.fetchone()
    if record[0] == 1:
        inpNewExpName = input("Enter new expense name: ")
        tableCategory()
        inpNewExpCat = input("Enter new expense category: ")
        inpNewExpCost = input("Enter new expense cost: ")
        c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpNewExpCat,))
        record = c.fetchone()
        if record[0] == 1:
            c.execute("UPDATE expenses SET (name, category, cost) = ('"+ inpNewExpName +"', '"+ inpNewExpCat +"', '"+ inpNewExpCost +"') WHERE eid = ('"+ inpExpense +"')")
            avgCost = pd.read_sql_query("SELECT (cost) FROM expenses WHERE name=('"+ inpNewExpName +"')", conn)
            totCost = pd.read_sql_query("SELECT SUM(cost) FROM expenses WHERE category=('"+ inpNewExpCat +"')", conn)
            avgBudget = pd.read_sql_query("SELECT (budget) FROM categories WHERE name=('" + inpNewExpCat + "') LIMIT 1", conn)
            avgExpense = (avgBudget.iloc[0,0] - avgCost.iloc[0,0])
            totExpense = (avgBudget.iloc[0,0] - totCost.iloc[0,0])
            c.execute("UPDATE expenses SET (overUnder) = ('"+ str(round(avgExpense, 2)) +"') WHERE name=('"+ inpNewExpName +"')")
            c.execute("UPDATE expenses SET (catTotal) = ('"+ str(round(totExpense, 2)) +"') WHERE category=('"+ inpNewExpCat +"')")
            conn.commit()
            print("Expense has been updated\n")
            printOptions()
        else:
            print("Category does not exist, please try again or add new Category\n")
            printExpenseOptions()
    else:
        print("Expense does not exist, please try again or add new expense\n")
        printExpenseOptions()


def deleteExpense():
    print(" deleteExpense called\n")
    tableExpense()
    inpExpense = input("\nEnter expense to delete (case sensitive): ")
    c.execute("SELECT EXISTS(SELECT 1 FROM expenses WHERE name=? LIMIT 1)", (inpExpense,))
    record = c.fetchone()
    if record[0] == 1:
        c.execute("DELETE FROM expenses WHERE name = ('" + inpExpense + "')")
        conn.commit()
        print("Expense has been deleted\n")
        printOptions()
    else:
        print("Expense does not exist, please try again\n")
        printExpenseOptions()


###################### report functions ##########################

def graphExpense():
    print(" graphExpense called\n")
    dfTableExp = pd.read_sql_query("SELECT * FROM expenses", conn)
    with PdfPages("ExpenseReport.pdf") as pdf:
        dfTableExp.plot(kind='bar', x='name', y='cost', color='red')
        plt.title("Graph for all Expenses")
        plt.ylabel("Cost (£)")
        plt.xlabel("Expense")
        plt.legend()
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()
    conn.commit()
    print("Report generated in directory\n")
    printOptions()
    # get input from user of specified category
    # query db for expenses in specified category

def printPDFReportDWMY():
    print(" printPDFReportDWMY called\n")
    for key in reportDateOptions:
        val = reportDateOptions[key]
        print(key + val)
    selectedRepDateOption = input("Select an option by its key: ")
    if selectedRepDateOption == "q":
        conn.close()
        sys.exit(0)
    elif selectedRepDateOption == "1":
        #year func
        #inpYear = input("Enter year to view expenses of (YYYY): ")
        inpRepDate1 = input("Enter date to view over/under range from (YYYY-MM-DD): ")
        inpRepDate2 = input("Enter date to view over/under range to (YYYY-MM-DD): ")
        if len(inpRepDate1) and len(inpRepDate2) != 10:
            print("Invalid date, please try again")
            printReportOptions()
        else:
            dfTableDate = pd.read_sql_query("SELECT * FROM expenses WHERE date BETWEEN '"+ inpRepDate1 +"' AND '"+ inpRepDate2 +"' ", conn)
            with PdfPages("reports/Expenses "+ inpRepDate1 +" to "+ inpRepDate2 +".pdf") as pdf:
                dfTableDate.plot(kind='bar', x='name', y='cost', color='red')
                plt.title("Expenses "+ inpRepDate1 +" to "+ inpRepDate2 +"")
                plt.ylabel("Cost (£)")
                plt.xlabel("Expense")
                plt.legend()
                pdf.savefig()
                plt.close()
            conn.commit()
            print("Report generated in directory\n")
            printOptions()

    elif selectedRepDateOption == "2":
        inpDay = input("Enter day to view expenses of (YYYY-MM-DD): ")
        c.execute("SELECT EXISTS(SELECT 1 FROM expenses WHERE date=? LIMIT 1)", (inpDay,))
        record = c.fetchone()
        if record[0] == 1:
            dfDateExp = pd.read_sql_query("SELECT * FROM expenses WHERE date=('" + inpDay + "')", conn)
            with PdfPages("reports/"+ inpDay +" Expense Report.pdf") as pdf:
                dfDateExp.plot(kind='bar', x='name', y='cost', color='red')
                plt.title("Expenses from "+ inpDay +"")
                plt.ylabel("Cost (£)")
                plt.xlabel("Expense")
                plt.legend()
                pdf.savefig()
                plt.close()
            conn.commit()
            print("Report generated in directory\n")
            printOptions()
        else:
            print("Date does not exist, please try again or add expense")
            printReportOptions()

    elif selectedRepDateOption == "b":
        printReportOptions()
    # get input from user of the date
    # query db category expenses and then print the list to a pdf using panda/matploblib ?


def printPDFReportByCategory():
    print(" printPDFReportByCategory called\n")
    tableCategory()
    inpRepCat = input("Enter category to view expense report of: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpRepCat,))
    record = c.fetchone()
    if record[0] == 1:
        dfTableExpCat = pd.read_sql_query("SELECT * FROM expenses WHERE category=('" + inpRepCat + "')", conn)
        with PdfPages("/reports/"+ inpRepCat +" Expense Report.pdf") as pdf:
            dfTableExpCat.plot(kind='bar', x='name', y='cost', color='blue')
            plt.title("Expenses for Category: " + inpRepCat)
            plt.ylabel("Cost (£)")
            plt.xlabel("Expense")
            plt.legend()
            pdf.savefig()  # saves the current figure into a new page in pdf 
            plt.close()
        conn.commit()
        print("Report generated in reports folder\n")
        printOptions()
    else:
        print("Category does not exist, please try again or add new category\n")
        printReportOptions()
    # get input from user of specified category
    # query db category expenses and then print the list to a pdf using panda/matploblib ?

def avgOverUnder():
    print(" avgOverUnder called\n")
    tableCategory()
    inpRepOverUnder = input("Enter category to view over/under report of: ")
    inpRepDate1 = input("Enter date to view over/under range from (YYYY-MM-DD): ")
    inpRepDate2 = input("Enter date to view over/under range to (YYYY-MM-DD): ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpRepOverUnder,))
    record = c.fetchone()
    if record[0] == 1:
        dfTableDate = pd.read_sql_query("SELECT * FROM expenses WHERE category =('"+ inpRepOverUnder +"') AND date BETWEEN '"+ inpRepDate1 +"' AND '"+ inpRepDate2 +"' ", conn)
        with PdfPages("OverUnder "+ inpRepOverUnder +".pdf") as pdf:
            # colours = ['blue' if ( y >0) else 'red']
            dfTableDate.plot(kind='bar', x='name', y='overUnder', color= 'blue')
            plt.title("Over/Under for Category: " + inpRepOverUnder)
            plt.ylabel("Over/Under ('-' = over)")
            plt.xlabel("Expense")
            plt.legend()
            pdf.savefig() # saves the current figure into a new page in pdf 
            plt.close()
        conn.commit()
        print("Report generated in directory\n")
        printOptions()
    else:
        print("Category does not exist, please try again or add new category\n")
        printReportOptions()


def exportExpensesToExcel():
    print(" exportExpensesToExcel called\n")
    dfTableInc = pd.read_sql_query("SELECT * FROM mIncome", conn)
    dfTableCat = pd.read_sql_query("SELECT * FROM categories", conn)
    dfTableExp = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.commit()

    writer = pd.ExcelWriter('reports/expenseSheet.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Expense Data')
    writer.sheets['Expense Data'] = worksheet
    dfTableInc.to_excel(writer, sheet_name='Expense Data',startrow=0, startcol=0)
    dfTableCat.to_excel(writer, sheet_name='Expense Data',startrow=0, startcol=6)
    dfTableExp.to_excel(writer, sheet_name='Expense Data',startrow=0, startcol=11)
    workbook.close()

    print("Data in 4 tables exported successfully\n")
    printOptions()

##################################################################

################### start program ################################


print("Welcome to your Expense Manager")
print("Please choose from the following options:\n")
printOptions()


##################################################################

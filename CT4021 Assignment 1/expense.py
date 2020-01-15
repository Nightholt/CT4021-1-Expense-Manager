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
    "q": " - Quit from any menu\n"
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
    if selectedOption == "q": #close db and quit program if 'q' pressed
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

# func to print income table for user to select from that looks nice
def tableIncome():
    table = pd.read_sql_query("SELECT * FROM mIncome", conn)
    print(table)
    conn.commit()

# function to calculate total income and insert into total column
def updateTotal():
    incomeTotal = pd.read_sql_query("SELECT SUM(income) FROM mIncome", conn)
    c.execute("UPDATE mIncome SET (total) = ('" + str(incomeTotal.iloc[0,0]) + "')")

# add new income
def setMonthlyIncome():
    print(" setMonthlyIncome called\n")
    inpSource = input("Enter name of source: ")
    inpIncome = input("Enter monthly income: £")
    c.execute("INSERT INTO mIncome (source, income) VALUES ('" + inpSource + "', '" + inpIncome +"')") #insert user inputs into correct columns in db
    updateTotal() #called to calculate total
    conn.commit()
    print("Income has been saved\n")
    printOptions() #back to main menu
   
# update existing income
def updateMonthlyIncome():
    print(" updateMonthlyIncome called\n")
    tableIncome() #call table for user to see what sources to choose from
    inpSource = input("\nEnter source name to update by mid: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM mIncome WHERE mid=? LIMIT 1)", (inpSource,)) #check input is valid, otherwise back to menu
    record = c.fetchone()
    if record[0] == 1: #only works if source exists
        inpIncome = input("Enter a new income: £")
        c.execute("UPDATE mIncome SET (income) = (" + inpIncome +") WHERE mid = ('" + inpSource + "')") #replace old value with new
        updateTotal()
        print("Income has been updated\n")
        printOptions()
    else:
        print("Source does not exist, please try again or add new source\n")
        printIncomeOptions()


def deleteMonthlyIncome():
    print(" deleteMonthlyIncome called\n")
    tableIncome() #call table for user to see what sources to choose from
    inpSource = input("\nEnter income source to delete by mid: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM mIncome WHERE mid=? LIMIT 1)", (inpSource,)) #check valid input
    record = c.fetchone()
    if record[0] == 1: #only works if source exists
        c.execute("DELETE FROM mIncome WHERE mid = ('" + inpSource + "')") #delete matching entry
        updateTotal()
        conn.commit()
        print("Income source has been deleted\n")
        printOptions()
    else:
        print("Source does not exist, please try again or add new source\n")
        printIncomeOptions()

###################### category functions ##########################

# func to print categories for user to select from that looks nice
def tableCategory():
    table = pd.read_sql_query("SELECT (name) FROM categories", conn)
    print(table)
    conn.commit()

# add new category
def addNewCategory():
    print(" addNewCategory called\n")
    inpCategory = input("Enter new category: ")
    c.execute("INSERT INTO categories (name) VALUES ('" + inpCategory + "')") #save to db category table in name column
    conn.commit()
    print("New category has been saved\n")
    printOptions() #back to main

# update existing category
def updateCategories():
    print(" updateCategories called\n")
    tableCategory() #call table for user to see what categories to choose from
    inpCategory = input("\nEnter category to update: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,)) #check input exists
    record = c.fetchone()
    if record[0] == 1: #only works if category exists
        inpNewCategory = input("Enter new category name: ")
        c.execute("UPDATE categories SET (name) = ('"+  inpNewCategory +"') WHERE name = ('"+ inpCategory +"')") #replce previous value with new
        conn.commit()
        print("Category has been updated\n")
        printOptions()
    else:
        print("Category does not exist, please try again\n")
        printCategoryOptions()

# delete existing category
def deleteCategories():
    print(" deleteCategories called\n")
    tableCategory() #call table for user to see what categories to choose from
    inpCategory = input("\nEnter category to delete: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,))
    record = c.fetchone()
    if record[0] == 1: #only works if category exists
        c.execute("DELETE FROM categories WHERE name = ('"+ inpCategory +"')")
        conn.commit()
        print("Category has been deleted\n")
        printOptions()
    else:
        print("Category does not exist, please try again\n")
        printCategoryOptions()

# set/update budget of category
def setCategoryBudget():
    print(" setCategoryBudget called\n")
    tableCategory() #call table for user to see what categories to choose from
    inpCategory = input("\nEnter category to add/update a budget for: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,)) #check exists
    record = c.fetchone()
    if record[0] == 1: #only works if category exists
        inpBudget = input("Enter a budget: £")
        #budget column updated where category name matches
        c.execute("UPDATE categories SET (budget) = ('"+ inpBudget +"') WHERE name = ('"+ inpCategory +"')") 
        conn.commit()
        print("budget has been saved\n")
        printOptions()
    else:
        print("Category does not exist, please try again or add new category\n")
        printCategoryOptions()


###################### expense functions ##########################

# func to print expenses for user to select from that looks nice
def tableExpense():
    table = pd.read_sql_query("SELECT * FROM expenses", conn) # creates dataframe from db selection
    print(table)
    conn.commit()

# add expense with category
def addCategoryExpense():
    print(" addCategoryExpense called\n")
    inpExpense = input("Enter expense name: ")
    tableCategory() #call table for user to see what categories to choose from
    inpCategory = input("\nEnter category to add expense to: ")
    inpCost = input("Enter expense cost: ")
    inpDate = input("Enter expense date(YYYY-MM-DD): ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpCategory,)) #check category exists
    record = c.fetchone()
    if record[0] == 1 and len(inpDate) == 10 and ("-", "-" in inpDate): #only works if category exists and date is correct
        #insert new values
        c.execute("INSERT INTO expenses (name, category, cost, date) VALUES ('" + inpExpense + "', '" + inpCategory + "', '" + inpCost + "', '" + inpDate + "')")
        #create dataframe of expense cost
        avgCost = pd.read_sql_query("SELECT (cost) FROM expenses WHERE name=('" + inpExpense + "')", conn)
        #dataframe for total
        totCost = pd.read_sql_query("SELECT SUM(cost) FROM expenses WHERE category=('"+ inpCategory +"')", conn)
        #create dataframe of category budget
        avgBudget = pd.read_sql_query("SELECT (budget) FROM categories WHERE name=('" + inpCategory + "') LIMIT 1", conn)
        avgExpense = (avgBudget.iloc[0,0] - avgCost.iloc[0,0]) #individual over/under for expense
        totExpense = (avgBudget.iloc[0,0] - totCost.iloc[0,0]) #total over/under for category
        #update individual over/under for expense
        c.execute("UPDATE expenses SET (overUnder) = ('"+ str(round(avgExpense, 2)) +"') WHERE name=('"+ inpExpense +"')") #value must be str before inserting
        #update total over/under for each expense in category
        c.execute("UPDATE expenses SET (catTotal) = ('"+ str(round(totExpense, 2)) +"') WHERE category=('"+ inpCategory +"')") #value must be str before inserting
        conn.commit()
        print("New expense has been saved\n")
        printOptions()
    else:
        print("Invalid category or date, please try again\n")
        printExpenseOptions()


def updateExpense():
    print(" updateExpense called\n")
    tableExpense() #call table for user to see what expenses to choose from
    inpExpense = input("\nEnter expense to update by eid: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM expenses WHERE eid=? LIMIT 1)", (inpExpense,))
    record = c.fetchone()
    if record[0] == 1: #only works if expense exists
        inpNewExpName = input("Enter new expense name: ")
        tableCategory()
        inpNewExpCat = input("Enter new expense category: ")
        inpNewExpCost = input("Enter new expense cost: ")
        c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpNewExpCat,)) #check exists
        record = c.fetchone()
        if record[0] == 1: #only works if category exists
            #replace old values with new
            c.execute("UPDATE expenses SET (name, category, cost) = ('"+ inpNewExpName +"', '"+ inpNewExpCat +"', '"+ inpNewExpCost +"') WHERE eid = ('"+ inpExpense +"')")
            #create dataframe of expense cost
            avgCost = pd.read_sql_query("SELECT (cost) FROM expenses WHERE name=('"+ inpNewExpName +"')", conn)
            #dataframe for total
            totCost = pd.read_sql_query("SELECT SUM(cost) FROM expenses WHERE category=('"+ inpNewExpCat +"')", conn)
            #create dataframe of category budget
            avgBudget = pd.read_sql_query("SELECT (budget) FROM categories WHERE name=('" + inpNewExpCat + "') LIMIT 1", conn)
            avgExpense = (avgBudget.iloc[0,0] - avgCost.iloc[0,0]) #individual over/under for expense
            totExpense = (avgBudget.iloc[0,0] - totCost.iloc[0,0]) #total over/under for category
            #update individual over/under for expense
            c.execute("UPDATE expenses SET (overUnder) = ('"+ str(round(avgExpense, 2)) +"') WHERE name=('"+ inpNewExpName +"')") #value must be str before inserting
            #update total over/under for each expense in category
            c.execute("UPDATE expenses SET (catTotal) = ('"+ str(round(totExpense, 2)) +"') WHERE category=('"+ inpNewExpCat +"')") #value must be str before inserting
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
    tableExpense() #call table for user to see what expenses to choose from
    inpExpense = input("\nEnter expense to delete by eid: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM expenses WHERE eid=? LIMIT 1)", (inpExpense,)) #check expense exists
    record = c.fetchone()
    if record[0] == 1: #only works if expense exists
        #create dataframe of expense cost
        avgCost = pd.read_sql_query("SELECT (cost) FROM expenses WHERE eid=('"+ inpExpense +"')", conn)
        #dataframe for total
        totCost = pd.read_sql_query("SELECT SUM(cost) FROM expenses WHERE category=( SELECT (category) FROM expenses WHERE eid=('" + inpExpense + "') LIMIT 1)", conn)
        #create dataframe of category budget
        avgBudget = pd.read_sql_query("SELECT (budget) FROM categories WHERE name=( SELECT (category) FROM expenses WHERE eid=('" + inpExpense + "') LIMIT 1) LIMIT 1", conn)
        totExpense = (avgBudget.iloc[0,0] - (totCost.iloc[0,0] - avgCost.iloc[0,0]) ) #total over/under for category
        #update total over/under for each expense in category
        c.execute("UPDATE expenses SET (catTotal) = ('"+ str(round(totExpense, 2)) +"') WHERE category=( SELECT (category) FROM expenses WHERE eid=('" + inpExpense + "') LIMIT 1)") #value must be str before inserting  
        c.execute("DELETE FROM expenses WHERE eid = ('"+ inpExpense +"')")
        conn.commit()
        print("Expense has been deleted\n")
        printOptions()
    else:
        print("Expense does not exist, please try again\n")
        printExpenseOptions()


###################### report functions ##########################

#create graph of all expenses
def graphExpense():
    print(" graphExpense called\n")
    dfTableExp = pd.read_sql_query("SELECT * FROM expenses", conn) #create dataframe to plot from
    with PdfPages("All Expenses.pdf") as pdf:
        dfTableExp.plot(kind='bar', x='name', y='cost', color='red') #define graph type, axis and colour
        plt.title("Graph for all Expenses")
        plt.ylabel("Cost (£)")
        plt.xlabel("Expense")
        plt.legend()
        pdf.savefig() #saves figure into a pdf page
        plt.close() #close figure
    conn.commit()
    print("Report generated in reports folder\n")
    printOptions()

#expense report by user input of day, week, month, year
def printPDFReportDWMY():
    print(" printPDFReportDWMY called\n")
    for key in reportDateOptions: #print options for report
        val = reportDateOptions[key]
        print(key + val)
    selectedRepDateOption = input("Select an option by its key: ")
    if selectedRepDateOption == "q": #close db and quit program if 'p' pressed
        conn.close()
        sys.exit(0)
    elif selectedRepDateOption == "1": #if option 1 selected
        #get input for range to select from
        inpRepDate1 = input("Enter date to view over/under range from (YYYY-MM-DD): ")
        inpRepDate2 = input("Enter date to view over/under range to (YYYY-MM-DD): ")
        if len(inpRepDate1) and len(inpRepDate2) != 10 and ("-", "-" in inpRepDate1 and inpRepDate2): #only works if dates are correct
            print("Invalid date, please try again")
            printReportOptions()
        else:
            #select all expense values between user defined range into dataframe
            dfTableDate = pd.read_sql_query("SELECT * FROM expenses WHERE date BETWEEN '"+ inpRepDate1 +"' AND '"+ inpRepDate2 +"' ", conn)
            #create pdf of graph from dataframe 
            with PdfPages("reports/Expenses "+ inpRepDate1 +" to "+ inpRepDate2 +".pdf") as pdf:
                dfTableDate.plot(kind='bar', x='name', y='cost', color='red') #define figure type, axis and colour
                plt.title("Expenses from "+ inpRepDate1 +" to "+ inpRepDate2 +"")
                plt.ylabel("Cost (£)")
                plt.xlabel("Expense")
                plt.legend()
                pdf.savefig() #save figure
                plt.close() #close figure
            conn.commit()
            print("Report generated in reports folder\n")
            printOptions()

    elif selectedRepDateOption == "2": #if option 2 selected
        #get input for exact day to view expenses from
        inpDay = input("Enter day to view expenses of (YYYY-MM-DD): ")
        c.execute("SELECT EXISTS(SELECT 1 FROM expenses WHERE date=? LIMIT 1)", (inpDay,)) #check date exists
        record = c.fetchone()
        if record[0] == 1: #only works if date exists
            #get all entries with matching date and add to dataframe
            dfDateExp = pd.read_sql_query("SELECT * FROM expenses WHERE date=('" + inpDay + "')", conn)
            #create pdf of graph from dataframe 
            with PdfPages("reports/"+ inpDay +" Expenses.pdf") as pdf:
                dfDateExp.plot(kind='bar', x='name', y='cost', color='red') #define figure type, axis and colour 
                plt.title("Expenses from "+ inpDay +"")
                plt.ylabel("Cost (£)")
                plt.xlabel("Expense")
                plt.legend()
                pdf.savefig() #save figure
                plt.close() #close figure
            conn.commit()
            print("Report generated in reports folder\n")
            printOptions()
        else:
            print("Date does not exist, please try again or add expense")
            printReportOptions()

    elif selectedRepDateOption == "b":
        printReportOptions()

#expense report by user selected category
def printPDFReportByCategory():
    print(" printPDFReportByCategory called\n")
    tableCategory() #call table for user to see what categories to choose from
    inpRepCat = input("Enter category to view expense report of: ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpRepCat,)) #check exists
    record = c.fetchone()
    if record[0] == 1: #only works if category exists
        #get all values with matching category and add to df
        dfTableExpCat = pd.read_sql_query("SELECT * FROM expenses WHERE category=('" + inpRepCat + "')", conn)
        #create pdf of graph from dataframe
        with PdfPages("/reports/"+ inpRepCat +" Expenses.pdf") as pdf:
            dfTableExpCat.plot(kind='bar', x='name', y='cost', color='blue')  #define figure type, axis and colour
            plt.title("Expenses for Category: " + inpRepCat)
            plt.ylabel("Cost (£)")
            plt.xlabel("Expense")
            plt.legend()
            pdf.savefig()  #save figure
            plt.close() #close figure
        conn.commit()
        print("Report generated in reports folder\n")
        printOptions()
    else:
        print("Category does not exist, please try again or add new category\n")
        printReportOptions()
    # get input from user of specified category
    # query db category expenses and then print the list to a pdf using panda/matploblib ?

#report of over/under for category in specified date range
def avgOverUnder():
    print(" avgOverUnder called\n")
    tableCategory() #call table for user to see what categories to choose from
    inpRepOverUnder = input("Enter category to view over/under report of: ")
    inpRepDate1 = input("Enter date to view over/under range from (YYYY-MM-DD): ")
    inpRepDate2 = input("Enter date to view over/under range to (YYYY-MM-DD): ")
    c.execute("SELECT EXISTS(SELECT 1 FROM categories WHERE name=? LIMIT 1)", (inpRepOverUnder,)) #check exists
    record = c.fetchone()
    if record[0] == 1: #only works if category exists
        #get all values with matching category in specific time frame and add to df 
        dfTableDate = pd.read_sql_query("SELECT * FROM expenses WHERE category =('"+ inpRepOverUnder +"') AND date BETWEEN '"+ inpRepDate1 +"' AND '"+ inpRepDate2 +"' ", conn)
        #create pdf of graph from dataframe
        with PdfPages("OverUnder "+ inpRepOverUnder +".pdf") as pdf:
            dfTableDate.plot(kind='bar', x='category', y='catTotal', color= 'blue')  #define figure type, axis and colour
            plt.title("Over/Under for Category: " + inpRepOverUnder)
            plt.ylabel("Over/Under ('-' = over)")
            plt.xlabel("Expense")
            plt.legend()
            pdf.savefig() #save figure
            plt.close() #close figure
        conn.commit()
        print("Report generated in reports folder\n")
        printOptions()
    else:
        print("Category does not exist, please try again or add new category\n")
        printReportOptions()

#export all data to excel
def exportExpensesToExcel():
    print(" exportExpensesToExcel called\n")
    #add each db table into a df 
    dfTableInc = pd.read_sql_query("SELECT * FROM mIncome", conn)
    dfTableCat = pd.read_sql_query("SELECT * FROM categories", conn)
    dfTableExp = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.commit()

    #use module to export to excel
    writer = pd.ExcelWriter('reports/Expense Sheet.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Expense Data') #worksheet name
    writer.sheets['Expense Data'] = worksheet #define where to add data
    #start each table with one gap between
    dfTableInc.to_excel(writer, sheet_name='Expense Data',startrow=0, startcol=0) 
    dfTableCat.to_excel(writer, sheet_name='Expense Data',startrow=0, startcol=6)
    dfTableExp.to_excel(writer, sheet_name='Expense Data',startrow=0, startcol=11)
    workbook.close()

    print("Data in 4 tables exported successfully\n Viewable in reports folder")
    printOptions()

##################################################################

################### start program ################################

#what user sees when program first launches
print("Welcome to your Expense Manager")
print("Please choose from the following options:\n")
printOptions()

##################################################################
#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv

if len(argv) == 2:
  FILENAME = 'sqlite:///' + argv[1]
else:
  FILENAME = 'sqlite:///money.db'

from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from sqlalchemy import create_engine, desc, and_
from sqlalchemy.orm import sessionmaker
from models import Base, Category, IncomeSource, ExpensesItem, IncomeItem, Variable, Shortcut
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# import locale
# locale.setlocale(locale.LC_ALL,'')

app = Flask(__name__)

engine = create_engine(FILENAME)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_date_object(all_rows):
  for row in all_rows:
    row.date_obj = datetime.strptime(row.date, "%Y-%m-%d").date()
  return all_rows

def first_of_current_month():
  now = datetime.now()
  return now + relativedelta(day=1)

def n_months_ago(n):
  now = datetime.now()
  return now + relativedelta(months = -n, day = 1)

def getAllIncomeRows(start_date, end_date):
  return session.query(IncomeItem).join("source").filter(IncomeItem.date.between(start_date, end_date)).order_by(IncomeItem.date.desc(),IncomeItem.id.desc()).all()

def getAllExpensesRows(start_date, end_date):
  return session.query(ExpensesItem).join("category").filter(ExpensesItem.date.between(start_date, end_date)).order_by(ExpensesItem.date.desc(),ExpensesItem.id.desc()).all()

######################################################

@app.route('/')
@app.route('/expenses/', methods = ['GET','POST'])
def Expenses():

  start_date = n_months_ago(2).strftime("%Y-%m-%d")
  current_date = datetime.now().strftime("%Y-%m-%d")

  if request.method == 'POST':

    if request.form['command'] == 'delete':

      deleted_id = request.form['id']
      deletedItem = session.query(ExpensesItem).filter_by(id=deleted_id).one()
      session.delete(deletedItem)
      session.commit()
      print "Deleted row " + deleted_id

      allExpensesRows = getAllExpensesRows(start_date, current_date)  

      add_date_object(allExpensesRows)
      allCategoryRows = session.query(Category).all()
      return render_template('expenses_table.html', 
                             allExpensesRows = allExpensesRows,
                             allCategoryRows = allCategoryRows)


    elif request.form['command'] == 'insert':

      input_date = request.form['date']
      input_amount = request.form['amount']
      input_category = request.form['category']
      input_description = request.form['description']
      expenseItem = ExpensesItem(date = input_date, 
                                 amount = input_amount, 
                                 category_id = input_category, 
                                 description = input_description)
      session.add(expenseItem)
      session.commit()
      print "Inserted row %s | %s | %s | %s" % (input_date, 
                                                input_amount,
                                                input_category, 
                                                input_description)
      
      allExpensesRows = getAllExpensesRows(start_date, current_date)  
      add_date_object(allExpensesRows)
      allCategoryRows = session.query(Category).all()
      return render_template('expenses_table.html', 
                              allExpensesRows = allExpensesRows,
                              allCategoryRows = allCategoryRows)


    elif request.form['command'] == 'update':

      input_id = request.form['id']
      input_field = request.form['field']
      input_value = request.form['value']

      row = session.query(ExpensesItem).filter_by(id=input_id).one()

      if input_field == 'date':
        row.date = input_value
      elif input_field == 'amount':
        row.amount = input_value
      elif input_field == 'category':
        row.category_id = input_value
      elif input_field == 'description':
        row.description = input_value

      session.commit()
      print "Updated row %s" % str(input_id)

      allExpensesRows = getAllExpensesRows(start_date, current_date)  
      add_date_object(allExpensesRows)
      allCategoryRows = session.query(Category).all()
      return render_template('expenses_table.html', 
                              allExpensesRows = allExpensesRows,
                              allCategoryRows = allCategoryRows)


  else:  # normal GET request

    allExpensesRows = getAllExpensesRows(start_date, current_date)  
    add_date_object(allExpensesRows)
    allCategoryRows = session.query(Category).all()
    allShortcuts = session.query(Shortcut).all()
    return render_template('expenses.html', 
                           allExpensesRows = allExpensesRows,
                           allCategoryRows = allCategoryRows,
                           allShortcuts = allShortcuts)


######################################################

@app.route('/income/', methods = ['GET','POST'])
def Income():

  start_date = n_months_ago(2).strftime("%Y-%m-%d")
  current_date = datetime.now().strftime("%Y-%m-%d")

  if request.method == 'POST':

    if request.form['command'] == 'delete':
      deleted_id = request.form['id']
      deletedItem = session.query(IncomeItem).filter_by(id=deleted_id).one()
      session.delete(deletedItem)
      session.commit()
      print "Deleted row " + deleted_id
      allIncomeRows = getAllIncomeRows(start_date, current_date)
      allSourceRows = session.query(IncomeSource).all()
      return render_template('income_table.html', 
                             allIncomeRows = allIncomeRows,
                             allSourceRows = allSourceRows)


    elif request.form['command'] == 'insert':
      input_date = request.form['date']
      input_amount = request.form['amount']
      input_source = request.form['source']
      input_description = request.form['description']
      incomeItem = IncomeItem(date = input_date, 
                              amount = input_amount, 
                              source_id = input_source, 
                              description = input_description)
      session.add(incomeItem)
      session.commit()
      print "Inserted row %s | %s | %s | %s" % (input_date, 
                                                input_amount,
                                                input_source, 
                                                input_description)
      allIncomeRows = getAllIncomeRows(start_date, current_date)
      allSourceRows = session.query(IncomeSource).all()
      return render_template('income_table.html', 
                              allIncomeRows = allIncomeRows,
                              allSourceRows = allSourceRows)


    elif request.form['command'] == 'update':
      input_id = request.form['id']
      input_field = request.form['field']
      input_value = request.form['value']

      row = session.query(IncomeItem).filter_by(id=input_id).one()

      if input_field == 'date':
        row.date = input_value
      elif input_field == 'amount':
        row.amount = input_value
      elif input_field == 'source':
        row.source_id = input_value
      elif input_field == 'description':
        row.description = input_value

      session.commit()
      print "Updated row %s" % str(input_id)

      allIncomeRows = getAllIncomeRows(start_date, current_date)
      allSourceRows = session.query(IncomeSource).all()
      return render_template('income_table.html', 
                              allIncomeRows = allIncomeRows,
                              allSourceRows = allSourceRows)

  else: # normal GET request

    allIncomeRows = getAllIncomeRows(start_date, current_date)
    allSourceRows = session.query(IncomeSource).all()
    # return "This is the main page."
    return render_template('income.html', 
                           allIncomeRows = allIncomeRows,
                           allSourceRows = allSourceRows)


######################################################

class Month:
  
  def __init__(self, date):
    self.date = date
    self.name = date.strftime("%B %Y")
    self.date_string = date.strftime("%Y-%m-%d")
    self.end_date = date + relativedelta(day=31)
    self.end_date_string = self.end_date.strftime("%Y-%m-%d")

def getMonthsArray(num_months):

  allCategoryRows = session.query(Category).all()
  allSourceRows = session.query(IncomeSource).all()

  # populate categoryNames with names of categories from db
  categoryNames = {}
  for row in allCategoryRows:
    categoryNames[row.id] = row.name

  # populate sourceNames with names of sources from db
  sourceNames = {}
  for row in allSourceRows:
    sourceNames[row.id] = row.name

  months = []
  months.append(Month(first_of_current_month())) 

  for i in range(1, num_months):
    months.append(Month(n_months_ago(i))) 

  for m in months:
    m.cat_totals = {}
    m.src_totals = {}
    for row in allCategoryRows:
      m.cat_totals[row.id] = 0
    for row in allSourceRows:
      m.src_totals[row.id] = 0
    m.total_expenses = 0
    m.total_income = 0
    m.expenses_rows = session.query(ExpensesItem).join("category").filter(ExpensesItem.date.between(m.date_string, m.end_date_string)).order_by(desc("date")).all()
    m.income_rows = session.query(IncomeItem).join("source").filter(IncomeItem.date.between(m.date_string, m.end_date_string)).order_by(desc("date")).all()
    for row in m.expenses_rows:
      m.total_expenses += row.amount
      m.cat_totals[row.category_id] += row.amount
    for row in m.income_rows:
      m.total_income += row.amount
      m.src_totals[row.source_id] += row.amount

  return months


@app.route('/overview/')
@app.route('/overview/month/')
def Overview():

  months = getMonthsArray(4)

  allCategoryRows = session.query(Category).all()
  allSourceRows = session.query(IncomeSource).all()

  # populate categoryNames with names of categories from db
  categoryNames = {}
  for row in allCategoryRows:
    categoryNames[row.id] = row.name

  # populate sourceNames with names of sources from db
  sourceNames = {}
  for row in allSourceRows:
    sourceNames[row.id] = row.name

  # get total expenses and income for current year

  return render_template('overview.html', 
                         months = months,
                         categoryNames = categoryNames,
                         sourceNames = sourceNames)


@app.route('/overview/year/')
def OverviewYear():

  months = getMonthsArray(12)

  allCategoryRows = session.query(Category).all()
  allSourceRows = session.query(IncomeSource).all()
  savingsRate = session.query(Variable).filter_by(name = 'savings_rate').one().value

  # populate categoryNames with names of categories from db
  categoryNames = {}
  for row in allCategoryRows:
    categoryNames[row.id] = row.name

  # populate sourceNames with names of sources from db
  sourceNames = {}
  for row in allSourceRows:
    sourceNames[row.id] = row.name

  totalYearlyIncome = 0
  totalYearlyExpenses = 0
  for m in months:
    totalYearlyIncome += m.total_income
    totalYearlyExpenses += m.total_expenses


  return render_template('overview_year.html', 
                         months = months,
                         categoryNames = categoryNames,
                         sourceNames = sourceNames,
                         savingsRate = savingsRate,
                         totalYearlyIncome = totalYearlyIncome,
                         totalYearlyExpenses = totalYearlyExpenses)

@app.route('/analysis/')
def Analysis():

  months = getMonthsArray(12)

  allCategoryRows = session.query(Category).all()
  allSourceRows = session.query(IncomeSource).all()

  all_exp_totals = []
  all_inc_totals = []
  all_cat_totals = {}
  avg_cat_totals = {}

  for row in months:
    all_exp_totals.append(row.total_expenses)
    all_inc_totals.append(row.total_income)

  for cat in allCategoryRows:
    all_cat_totals[cat.name] = []
    for month in months:
      # if month.cat_totals[cat.id] > 0:
      all_cat_totals[cat.name].append(month.cat_totals[cat.id])

  for cat in all_cat_totals:
    avg_cat_totals[cat] = sum(all_cat_totals[cat]) / float(len(all_cat_totals[cat]))

  avg_mth_exp = sum(all_exp_totals) / float(len(all_exp_totals))
  avg_mth_inc = sum(all_inc_totals) / float(len(all_inc_totals))

  print all_cat_totals
  print ''
  print avg_cat_totals


  result_str = '''
               Your average expenses are $%0.2f a month, or $%0.2f a year.<br><br>
               Your average income is $%0.2f a month, or $%0.2f a year.<br><br>
               ''' % ((avg_mth_exp / 100), (avg_mth_exp * 12 / 100), 
                     (avg_mth_inc / 100), (avg_mth_inc * 12 / 100))

  result_str += 'Average monthly expenses by category:<br><br>'

  for i in sorted(avg_cat_totals):
    result_str += (i + ': $%0.2f %s' + '<br>') % ((float(avg_cat_totals[i] / 100)), (all_cat_totals[i]))

  return result_str

@app.route('/new-category/')
def NewCategory():
  return "This is the new category page."

@app.context_processor
def utility_processor():
  def format_money(amount):
    result = format(float(amount)/100, ',.2f')
    if amount < 0:
      # replace hyphen with minus char
      result = result.replace('-', u'\u2212')
    return result
  return dict(format_money=format_money)

@app.template_filter('replace_hyphen')
def replace_hyphen(string):
    return string.replace('-', u'\u2212')

if __name__ == '__main__':
  # app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host='127.0.0.1', port=5000)
























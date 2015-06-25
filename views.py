#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from sqlalchemy import create_engine, desc, and_
from sqlalchemy.orm import sessionmaker
from models import Base, Category, IncomeSource, ExpensesItem, IncomeItem, Variable, Shortcut
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# import locale
# locale.setlocale(locale.LC_ALL,'')

app = Flask(__name__)

engine = create_engine('sqlite:///money.db')
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

# def two_months_ago():
#   now = datetime.now()
#   return now + relativedelta(months=-2, day=1)

# def three_months_ago():
#   now = datetime.now()
#   return now + relativedelta(months=-3, day=1)



######################################################

@app.route('/')
@app.route('/expenses/', methods = ['GET','POST'])
def Expenses():

  start_date = n_months_ago(3).strftime("%Y-%m-%d")

  if request.method == 'POST':

    if request.form['command'] == 'delete':

      deleted_id = request.form['id']
      deletedItem = session.query(ExpensesItem).filter_by(id=deleted_id).one()
      session.delete(deletedItem)
      session.commit()
      print "Deleted row " + deleted_id
      allExpensesRows = session.query(ExpensesItem).join("category").filter(ExpensesItem.date >= start_date).order_by(desc("date")).all()
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
      allExpensesRows = session.query(ExpensesItem).join("category").filter(ExpensesItem.date >= start_date).order_by(desc("date")).all()
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

      allExpensesRows = session.query(ExpensesItem).join("category").filter(ExpensesItem.date >= start_date).order_by(desc("date")).all()
      add_date_object(allExpensesRows)
      allCategoryRows = session.query(Category).all()
      return render_template('expenses_table.html', 
                              allExpensesRows = allExpensesRows,
                              allCategoryRows = allCategoryRows)


  else:  # normal GET request

    allExpensesRows = session.query(ExpensesItem).join("category").filter(ExpensesItem.date >= start_date).order_by(desc("date")).all()
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

  start_date = n_months_ago(3).strftime("%Y-%m-%d")

  if request.method == 'POST':

    if request.form['command'] == 'delete':
      deleted_id = request.form['id']
      deletedItem = session.query(IncomeItem).filter_by(id=deleted_id).one()
      session.delete(deletedItem)
      session.commit()
      print "Deleted row " + deleted_id
      allIncomeRows = session.query(IncomeItem).join("source").order_by(desc("date")).all()
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
      allIncomeRows = session.query(IncomeItem).join("source").order_by(desc("date")).all()
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

      allIncomeRows = session.query(IncomeItem).join("source").order_by(desc("date")).all()
      allSourceRows = session.query(IncomeSource).all()
      return render_template('income_table.html', 
                              allIncomeRows = allIncomeRows,
                              allSourceRows = allSourceRows)

  else: # normal GET request

    allIncomeRows = session.query(IncomeItem).join("source").order_by(desc("date")).all()
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

@app.route('/overview/')
def Overview():


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

  # start_date = three_months_ago().strftime("%Y-%m-%d")

  months = []
  months.append(Month(first_of_current_month())) 

  for i in range(1, 6):
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


  # get total expenses and income for current year





  return render_template('overview.html', 
                         months = months,
                         categoryNames = categoryNames,
                         sourceNames = sourceNames)

  # return render_template('overview.html', 
  #                        totalExpenses = totalExpenses, 
  #                        totalIncome = totalIncome, 
  #                        totalForEachCategory = totalForEachCategory,
  #                        categoryNames = categoryNames,
  #                        totalForEachSource = totalForEachSource,
  #                        sourceNames = sourceNames)

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

if __name__ == '__main__':
  # app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host='127.0.0.1', port=5000)
























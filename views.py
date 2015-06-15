#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Base, Category, IncomeSource, ExpensesItem, IncomeItem, Variable, Shortcut

# import locale
# locale.setlocale(locale.LC_ALL,'')

app = Flask(__name__)

engine = create_engine('sqlite:///money.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/expenses/', methods = ['GET','POST'])
def Expenses():
  if request.method == 'POST':
    if request.form['command'] == 'delete':
      deleted_id = request.form['id']
      deletedItem = session.query(ExpensesItem).filter_by(id=deleted_id).one()
      session.delete(deletedItem)
      session.commit()
      print "Deleted row " + deleted_id
      allExpensesRows = session.query(ExpensesItem).join("category").order_by(desc("date")).all()
      return render_template('expenses_table.html', allExpensesRows = allExpensesRows)
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
      allExpensesRows = session.query(ExpensesItem).join("category").order_by(desc("date")).all()
      return render_template('expenses_table.html', allExpensesRows = allExpensesRows)
  else:
    allExpensesRows = session.query(ExpensesItem).join("category").order_by(desc("date")).all()
    allCategoryRows = session.query(Category).all()
    allShortcuts = session.query(Shortcut).all()
    # return "This is the main page."
    return render_template('expenses.html', 
                           allExpensesRows = allExpensesRows,
                           allCategoryRows = allCategoryRows,
                           allShortcuts = allShortcuts)

@app.route('/income/')
def Income():
  allIncomeRows = session.query(IncomeItem).join("source").order_by(desc("date")).all()
  # return "This is the main page."
  return render_template('income.html', allIncomeRows = allIncomeRows)

@app.route('/overview/')
def Overview():
  allExpensesRows = session.query(ExpensesItem).join("category").order_by(desc("date")).all()
  allIncomeRows = session.query(IncomeItem).join("source").order_by(desc("date")).all()
  allCategoryRows = session.query(Category).all()

  # populate totalCategories with a 0 for each category_id
  totalCategories = {}
  categoryNames = {}
  for row in allCategoryRows:
    totalCategories[row.id] = 0
    categoryNames[row.id] = row.name

  totalExpenses = 0
  totalIncome = 0

  for row in allExpensesRows:
    totalExpenses += row.amount
    totalCategories[row.category_id] += row.amount

  for row in allIncomeRows:
    totalIncome += row.amount

  return render_template('overview.html', 
                         totalExpenses = totalExpenses, 
                         totalIncome = totalIncome, 
                         totalCategories = totalCategories,
                         categoryNames = categoryNames)

@app.route('/new-category/')
def NewCategory():
  return "This is the new category page."

@app.context_processor
def utility_processor():
  def format_money(amount):
    # return locale.currency(float(amount)/100, grouping=True)
    return format(float(amount)/100, ',.2f')
  return dict(format_money=format_money)

if __name__ == '__main__':
  # app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host='127.0.0.1', port=5000)























#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv

if len(argv) == 2:
  FILENAME = 'sqlite:///' + argv[1]
else:
  FILENAME = 'sqlite:///money.db'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

from models import Base, Category, IncomeSource, ExpensesItem, IncomeItem, Variable, Shortcut

engine = create_engine(FILENAME)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

cat_rent = Category(name="Rent")
session.add(cat_rent)
cat_gas = Category(name="Gas")
session.add(cat_gas)
cat_water = Category(name="Water")
session.add(cat_water)
cat_electricity = Category(name="Electricity")
session.add(cat_electricity)
cat_internet = Category(name="Internet")
session.add(cat_internet)
cat_phone = Category(name="Phone")
session.add(cat_phone)
cat_pt = Category(name="Public transport")
session.add(cat_pt)
cat_groceries = Category(name="Groceries")
session.add(cat_groceries)
cat_eo = Category(name="Eating out")
session.add(cat_eo)
cat_clothes = Category(name="Clothes")
session.add(cat_clothes)
cat_haircuts = Category(name="Haircuts")
session.add(cat_haircuts)
cat_leisure = Category(name="Leisure")
session.add(cat_leisure)
cat_gym = Category(name="Gym")
session.add(cat_gym)
cat_petrol = Category(name="Petrol")
session.add(cat_petrol)
cat_media = Category(name="Media")
session.add(cat_media)
cat_equipment = Category(name="Equipment")
session.add(cat_equipment)
cat_gifts = Category(name="Gifts")
session.add(cat_gifts)
cat_donations = Category(name="Donations")
session.add(cat_donations)
cat_oneoffs = Category(name="One-offs")
session.add(cat_oneoffs)
cat_other = Category(name="Other")
session.add(cat_other)

session.commit()


sht = Shortcut(id=1, value="r") # R (82)
session.add(sht)
session.commit()
sht = Shortcut(id=8, value="g") # G (71)
session.add(sht)
session.commit()
sht = Shortcut(id=9, value="e") # E (69)
session.add(sht)
session.commit()
sht = Shortcut(id=6, value="p")
session.add(sht)
session.commit()
sht = Shortcut(id=7, value="t")
session.add(sht)
session.commit()
sht = Shortcut(id=10, value="c")
session.add(sht)
session.commit()
sht = Shortcut(id=11, value="h")
session.add(sht)
session.commit()
sht = Shortcut(id=20, value="o")
session.add(sht)
session.commit()


sr = Variable(name="savings_rate", value=0.5)
session.add(sr)
session.commit()


src_job = IncomeSource(name="Job")
session.add(src_job)
session.commit()

src_makojob = IncomeSource(name="Partner's job")
session.add(src_makojob)
session.commit()

src_tshirts = IncomeSource(name="T-shirts")
session.add(src_tshirts)
session.commit()

src_tax = IncomeSource(name="Tax return")
session.add(src_tax)
session.commit()

src_gifts = IncomeSource(name="Gifts")
session.add(src_gifts)
session.commit()


# expense1 = ExpensesItem(date="2015-06-12", amount=1750, description="Better Burger", category=cat_eo)
# expense2 = ExpensesItem(date="2015-06-11", amount=570, description="Hair wax", category=cat_groceries)
# expense3 = ExpensesItem(date="2015-06-10", amount=1230, category=cat_groceries)
# expense4 = ExpensesItem(date="2015-05-17", amount=4999, category=cat_phone)
# expense5 = ExpensesItem(date="2015-06-13", amount=1250, category=cat_eo, description="Renkon")
# expense6 = ExpensesItem(date="2015-04-20", amount=1000, category=cat_groceries)
# expense7 = ExpensesItem(date="2015-06-15", amount=5200, category=cat_gym)
# expense8 = ExpensesItem(date="2015-06-15", amount=11173, category=cat_electricity)
# expense9 = ExpensesItem(date="2015-06-15", amount=1200, category=cat_eo)
# expense10 = ExpensesItem(date="2015-06-15", amount=1270, category=cat_groceries)
# expense11 = ExpensesItem(date="2015-06-15", amount=550, category=cat_eo)
# expense12 = ExpensesItem(date="2015-06-15", amount=1038, category=cat_groceries)
# expense13 = ExpensesItem(date="2015-06-15", amount=850, category=cat_groceries)
# expense14 = ExpensesItem(date="2015-06-15", amount=1190, category=cat_eo)
# expense15 = ExpensesItem(date="2015-06-15", amount=1787, category=cat_groceries)
# expense16 = ExpensesItem(date="2015-06-16", amount=7500, category=cat_internet)
# expense17 = ExpensesItem(date="2015-05-12", amount=500, category=cat_haircuts)
# expense18 = ExpensesItem(date="2015-05-01", amount=1737, category=cat_groceries)
# expense19 = ExpensesItem(date="2015-05-11", amount=913, category=cat_eo)
# expense20 = ExpensesItem(date="2015-05-14", amount=12187, category=cat_gym)
# expense21 = ExpensesItem(date="2015-05-19", amount=123, category=cat_groceries)
# expense22 = ExpensesItem(date="2015-05-25", amount=3488, category=cat_eo)
# expense23 = ExpensesItem(date="2015-05-31", amount=1200, category=cat_groceries)
# expense24 = ExpensesItem(date="2015-05-24", amount=19382, category=cat_water)
# expense25 = ExpensesItem(date="2015-05-17", amount=1238, category=cat_groceries)
# expense26 = ExpensesItem(date="2015-04-13", amount=9999, category=cat_groceries)
# expense27 = ExpensesItem(date="2015-04-16", amount=1382, category=cat_phone)
# expense28 = ExpensesItem(date="2015-04-11", amount=1101, category=cat_groceries)
# expense29 = ExpensesItem(date="2015-04-05", amount=1874, category=cat_eo)
# expense30 = ExpensesItem(date="2015-04-21", amount=1091, category=cat_clothes)
# expense31 = ExpensesItem(date="2015-04-23", amount=538, category=cat_groceries)
# expense32 = ExpensesItem(date="2015-04-16", amount=99, category=cat_groceries)
# expense33 = ExpensesItem(date="2015-04-17", amount=250, category=cat_eo)
# expense34 = ExpensesItem(date="2015-04-10", amount=1180, category=cat_eo)

# session.add(expense1)
# session.add(expense2)
# session.add(expense3)
# session.add(expense4)
# session.add(expense5)
# session.add(expense6)
# session.add(expense7)
# session.add(expense8)
# session.add(expense9)
# session.add(expense10)
# session.add(expense11)
# session.add(expense12)
# session.add(expense13)
# session.add(expense14)
# session.add(expense15)
# session.add(expense16)
# session.add(expense17)
# session.add(expense18)
# session.add(expense19)
# session.add(expense20)
# session.add(expense21)
# session.add(expense22)
# session.add(expense23)
# session.add(expense24)
# session.add(expense25)
# session.add(expense26)
# session.add(expense27)
# session.add(expense28)
# session.add(expense29)
# session.add(expense30)
# session.add(expense31)
# session.add(expense32)
# session.add(expense33)
# session.add(expense34)

# income1 = IncomeItem(date="2015-06-11", amount=202932, source=src_job,
#                      description="just got a raise")
# income2 = IncomeItem(date="2015-05-23", amount=2789, source=src_tshirts)
# income3 = IncomeItem(date="2015-06-12", amount=300, source=src_gifts)
# income4 = IncomeItem(date="2015-06-13", amount=220000, source=src_tax)
# income5 = IncomeItem(date="2015-05-30", amount=78900, source=src_makojob)

# session.add(income1)
# session.add(income2)
# session.add(income3)
# session.add(income4)
# session.add(income5)

# session.commit()

# populate expenses table



for y in range(2014, 2016):

  for i in range(1,13):

    # add a random number of expense items per month
    for t in range(random.randint(25, 61)):

      random_amt = random.randint(500,5000)
      day = str(random.randint(1,28)).zfill(2)
      month = str(i).zfill(2)
      year = str(y)
      random_category_id = random.randint(1, 20)
      random_date = '%s-%s-%s' % (year, month, day)

      random_expense = ExpensesItem(date = random_date,
                                    amount = random_amt,
                                    category_id = random_category_id)
      session.add(random_expense)
      session.commit()


# populate income table


for y in range(2014, 2016):

  for i in range(1,13):

    random_amt = random.randrange(300000,700000,10000)
    day = str(random.randint(1,28)).zfill(2)
    month = str(i).zfill(2)
    year = str(y)
    # year = str(random.randint(2014,2015))
    random_src_id = random.randint(1, 5)
    random_date = '%s-%s-%s' % (year, month, day)

    random_income = IncomeItem(date = random_date,
                               amount = random_amt,
                               source_id = random_src_id)
    session.add(random_income)
    session.commit()


print "DB population successful."






















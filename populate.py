#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, IncomeSource, ExpensesItem, IncomeItem, Variable, Shortcut

engine = create_engine('sqlite:///money.db')
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


sht = Shortcut(id=1, value=82) # R
session.add(sht)
session.commit()
sht = Shortcut(id=7, value=71) # G
session.add(sht)
session.commit()
sht = Shortcut(id=8, value=69) # E
session.add(sht)
session.commit()


src_job = IncomeSource(name="Job")
session.add(src_job)
session.commit()

src_makojob = IncomeSource(name="Mako's job")
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


expense1 = ExpensesItem(date="2015-06-12", amount=1750, description="Better Burger",
                        category=cat_eo)
expense2 = ExpensesItem(date="2015-06-11", amount=570, description="Hair wax",
                        category=cat_groceries)
expense3 = ExpensesItem(date="2015-06-10", amount=1230, category=cat_groceries)
expense4 = ExpensesItem(date="2015-05-17", amount=4999, category=cat_phone)
expense5 = ExpensesItem(date="2015-06-13", amount=1250, category=cat_eo, description="Renkon")
expense6 = ExpensesItem(date="2015-04-20", amount=1000, category=cat_groceries)

session.add(expense1)
session.add(expense2)
session.add(expense3)
session.add(expense4)
session.add(expense5)
session.add(expense6)

income1 = IncomeItem(date="2015-06-11", amount=202932, source=src_job,
                     description="just got a raise")
income2 = IncomeItem(date="2015-05-23", amount=2789, source=src_tshirts)
income3 = IncomeItem(date="2015-06-12", amount=300, source=src_gifts)
income4 = IncomeItem(date="2015-06-13", amount=220000, source=src_tax)
income5 = IncomeItem(date="2015-05-30", amount=78900, source=src_makojob)

session.add(income1)
session.add(income2)
session.add(income3)
session.add(income4)
session.add(income5)

session.commit()




print "DB population complete."






















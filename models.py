import os
import sys
from sys import argv

if len(argv) == 2:
  FILENAME = 'sqlite:///' + argv[1]
else:
  FILENAME = 'sqlite:///money.db'

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key = True)
  name = Column(String(30), nullable = False)

class IncomeSource(Base):
  __tablename__ = 'income_sources'

  id = Column(Integer, primary_key = True)
  name = Column(String(30), nullable = False)

class Shortcut(Base):
  __tablename__ = 'shortcuts'

  id = Column(Integer, primary_key = True)
  value = Column(String(3), nullable = False)

class ExpensesItem(Base):
  __tablename__ = 'expenses'

  id = Column(Integer, primary_key = True)
  date = Column(String(10), nullable = False)
  amount = Column(Integer, nullable = False)
  category_id = Column(Integer, ForeignKey('categories.id'))
  category = relationship(Category)
  description = Column(String(50))

class IncomeItem(Base):
  __tablename__ = 'income'

  id = Column(Integer, primary_key = True)
  date = Column(String(10), nullable = False)
  amount = Column(Integer, nullable = False)
  source_id = Column(Integer, ForeignKey('income_sources.id'))
  source = relationship(IncomeSource)
  description = Column(String(50))

class Variable(Base):
  __tablename__ = 'variables'

  name = Column(String(24), primary_key = True)
  value = Column(Integer, nullable = False)

  # @property
  # def serialize(self):
  #   #Returns object data in easily serializeable format
  #   return {
  #     'name': self.name,
  #     'description': self.description,
  #     'id': self.id,
  #     'price': self.price,
  #     'course': self.course,
  #   }


engine = create_engine(FILENAME)

Base.metadata.create_all(engine)
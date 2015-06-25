from datetime import datetime
from dateutil.relativedelta import relativedelta


def first_of_current_month():
  now = datetime.now()
  return now + relativedelta(day=1)

def one_month_ago():
  now = datetime.now()
  return now + relativedelta(months=-1, day=1)

def two_months_ago():
  now = datetime.now()
  return now + relativedelta(months=-2, day=1)

def three_months_ago():
  now = datetime.now()
  return now + relativedelta(months=-3, day=1)

class Month:
  def __init__(self, date):
    self.date = date
    self.name = date.strftime("%B %Y")
    self.date_string = date.strftime("%Y-%m-%d")
    self.end_date = date + relativedelta(day=31)


months = []
months.append(Month(first_of_current_month())) 
months.append(Month(one_month_ago())) 
months.append(Month(two_months_ago())) 
months.append(Month(three_months_ago())) 

for m in months:
  print m.date
  print m.name
  print m.date_string
  print 'end date:' + str(m.end_date)
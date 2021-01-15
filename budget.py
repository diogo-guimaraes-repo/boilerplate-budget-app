import math

class Category:
  
  def __init__(self, cat_name):
    self.ledger = []
    self.name = cat_name
    self.balance = 0

  def __str__(self):
    
    header = self.name.center(30, "*") + "\n"
    items = ""
    total = "Total: " + str(self.balance)

    for item in self.ledger:
      description = item["description"][0:23].ljust(23, " ")
      amount = float(item["amount"])
      amount = str("{:.2f}".format(amount))[0:7].rjust(7, " ")
      items += description + amount + "\n"

    return header + items + total

  def deposit(self, amount, description=""):
    self.balance += amount
    
    self.add_operation_to_ledger(amount, description)

  def withdraw(self, amount, description=""):
    ret = False

    if self.check_funds(amount) == True:
      self.balance -= amount
      self.add_operation_to_ledger(-amount, description)
      ret = True

    return ret

  def add_operation_to_ledger(self, amount, description):
    deposit = {
      "amount": amount,
      "description": description
    }
    self.ledger.append(deposit)

  def get_balance(self):
    return self.balance

  def check_funds(self, amount):
    ret = True
    if amount > self.balance:
      ret = False

    return ret

  def transfer(self, amount, dest_cat):
    
    ret = False
    if self.withdraw(amount, "Transfer to " + dest_cat.name) == True:
      dest_cat.deposit(amount, "Transfer from " + self.name)
      ret = True

    return ret

def create_spend_chart(categories):
    pairs = []
    total_spent = 0

    for category in categories:
      total_spent += calculate_spending(category)

    for category in categories:
      add_percentage_to_cat(category, round(round_down(calculate_spending(category)/total_spent)*100), pairs)

    return draw_chart(pairs)

def round_down(number, decimals=1):
  factor = 10 ** decimals
  return math.floor(number * factor) / factor

def draw_chart(pairs):
  header = "Percentage spent by category" + "\n"

  percentage_chart = draw_percentages(pairs)
  
  categories_chart = draw_categories(pairs)

  return header+percentage_chart+categories_chart

def draw_percentages(pairs):
  sep_length = len(pairs)*3+1
  chart = ""

  for curr_percentage in range(100, -10 , -10):
    chart += str(curr_percentage).rjust(3) + "| "
    for i, pair in enumerate(pairs):
      if pair["percentage"] >= curr_percentage:
        chart += "o  "
      else:
        for j in range(3):
          chart += " "
      if i == len(pairs)-1:
        chart += "\n"

  chart += "    "
  for i in range(sep_length):
    chart += "-"
    if i == sep_length-1:
      chart += "\n"      

  return chart

def draw_categories(pairs):
  chart = ""
  max_name_len = 0
  
  for pair in pairs:
    if len(pair["category_name"]) > max_name_len:
      max_name_len = len(pair["category_name"])
 
  for i in range(max_name_len):
    chart += "    "
    for j, pair in enumerate(pairs):
      cat_name = pair["category_name"]
      if i < len(cat_name):
        chart += cat_name[i].center(3, " ")
      else:
        for k in range(3):
          chart += " "

      if j == len(pairs)-1:
        chart += " "
        if i < max_name_len-1:
          chart += "\n"

  return chart


def add_percentage_to_cat(category, percentage, pairs):
  pair = {
    "category_name": category.name,
    "percentage": percentage
  }
  pairs.append(pair)



def calculate_spending(category):
  amount_spent = 0
  for item in category.ledger:
    if item["amount"] < 0:
      amount_spent += -item["amount"]
  
  return amount_spent
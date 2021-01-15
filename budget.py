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
    pass

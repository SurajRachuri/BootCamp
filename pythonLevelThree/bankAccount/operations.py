from decimal import Decimal
from models import Bank


def get_account(bank: Bank):
    acc = input("Account number: ")
    return bank.accounts.get(acc)


def create_account(bank):
    t = input("Type (savings/checking/business): ")
    name = input("Owner: ")
    amt = Decimal(input("Initial deposit: "))
    acc = bank.create_account(t, name, amt)
    print("Account created:", acc.account_number)


def deposit(bank):
    acc = get_account(bank)
    if not acc:
        return print("Account not found")
    acc.deposit(Decimal(input("Amount: ")))
    print("Deposit successful")


def withdraw(bank):
    acc = get_account(bank)
    if not acc:
        return print("Account not found")
    if acc.withdraw(Decimal(input("Amount: "))):
        print("Withdrawal successful")
    else:
        print("Withdrawal failed")


def transfer(bank):
    a = input("From: ")
    b = input("To: ")
    amt = Decimal(input("Amount: "))
    print("Success" if bank.transfer(a, b, amt) else "Failed")
def newOne(data):
    i=10
    b=data
    return i+b

def statement(bank):
    acc = get_account(bank)
    if acc:
        print(acc.get_statement())

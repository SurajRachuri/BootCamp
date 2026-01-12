from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    INTEREST = "interest"
    FEE = "fee"


@dataclass
class Transaction:
    type: TransactionType
    amount: Decimal
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = ""
    balance_after: Decimal = Decimal("0")


class Account(ABC):
    def __init__(self, account_number: str, owner: str, initial_balance: Decimal):
        self.account_number = account_number
        self.owner = owner
        self._balance = initial_balance
        self.transactions: List[Transaction] = []

    @property
    def balance(self):
        return self._balance

    def _record(self, t_type, amount, desc=""):
        self.transactions.append(
            Transaction(t_type, amount, description=desc, balance_after=self._balance)
        )

    def deposit(self, amount: Decimal):
        if amount <= 0:
            return False
        self._balance += amount
        self._record(TransactionType.DEPOSIT, amount)
        return True

    @abstractmethod
    def withdraw(self, amount: Decimal):
        pass

    @abstractmethod
    def calculate_interest(self):
        pass

    def get_statement(self):
        lines = [f"\n--- Statement {self.account_number} ({self.owner}) ---"]
        for t in self.transactions:
            lines.append(
                f"{t.timestamp} | {t.type.value} | ₹{t.amount} | Balance: ₹{t.balance_after}"
            )
        return "\n".join(lines)


class SavingsAccount(Account):
    RATE = Decimal("0.02")

    def withdraw(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        self._record(TransactionType.WITHDRAWAL, amount)
        return True

    def calculate_interest(self):
        interest = self._balance * self.RATE / 12
        self._balance += interest
        self._record(TransactionType.INTEREST, interest)


class CheckingAccount(Account):
    OVERDRAFT = Decimal("500")
    FEE = Decimal("35")

    def withdraw(self, amount):
        if self._balance + self.OVERDRAFT < amount:
            return False
        self._balance -= amount
        if self._balance < 0:
            self._balance -= self.FEE
            self._record(TransactionType.FEE, self.FEE)
        self._record(TransactionType.WITHDRAWAL, amount)
        return True

    def calculate_interest(self):
        pass


class BusinessAccount(Account):
    RATE = Decimal("0.01")

    def withdraw(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        self._record(TransactionType.WITHDRAWAL, amount)
        return True

    def calculate_interest(self):
        interest = self._balance * self.RATE / 12
        self._balance += interest
        self._record(TransactionType.INTEREST, interest)


class Bank:
    def __init__(self):
        self.accounts = {}
        self._next = 1001

    def create_account(self, acc_type, owner, deposit):
        acc_no = str(self._next)
        self._next += 1

        if acc_type == "savings":
            acc = SavingsAccount(acc_no, owner, deposit)
        elif acc_type == "checking":
            acc = CheckingAccount(acc_no, owner, deposit)
        else:
            acc = BusinessAccount(acc_no, owner, deposit)

        self.accounts[acc_no] = acc
        return acc

    def transfer(self, a, b, amt):
        if a not in self.accounts or b not in self.accounts:
            return False
        if self.accounts[a].withdraw(amt):
            self.accounts[b].deposit(amt)
            return True
        return False

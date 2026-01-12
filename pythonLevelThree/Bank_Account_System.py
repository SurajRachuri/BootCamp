# Full OOP implementation
# Requirements:
# - Abstract Account base class
# - SavingsAccount, CheckingAccount, BusinessAccount
# - Transaction history with timestamps
# - Interest calculation (different rates per type)
# - Overdraft protection for Checking
# - Transfer between accounts
# - Generate account statements

# Full OOP implementation
# Requirements:
# - Abstract Account base class
# - SavingsAccount, CheckingAccount, BusinessAccount
# - Transaction history with timestamps
# - Interest calculation (different rates per type)
# - Overdraft protection for Checking
# - Transfer between accounts
# - Generate account statements

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
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
    def __init__(self, account_number: str, owner: str, initial_balance: Decimal = Decimal("0")):
        self.account_number = account_number
        self.owner = owner
        self._balance = initial_balance
        self.transactions: List[Transaction] = []
        self.is_active = True

    @property
    def balance(self) -> Decimal:
        return self._balance

    def _record_transaction(self, t_type: TransactionType, amount: Decimal, description: str = ""):
        txn = Transaction(
            type=t_type,
            amount=amount,
            description=description,
            balance_after=self._balance
        )
        self.transactions.append(txn)

    def deposit(self, amount: Decimal, description: str = "") -> bool:
        if amount <= 0:
            return False
        self._balance += amount
        self._record_transaction(TransactionType.DEPOSIT, amount, description)
        return True

    @abstractmethod
    def withdraw(self, amount: Decimal) -> bool:
        pass

    @abstractmethod
    def calculate_interest(self) -> Decimal:
        pass

    def get_statement(self, start_date: datetime = None, end_date: datetime = None) -> str:
        statement_lines = [
            f"\n--- Account Statement for {self.owner} ({self.account_number}) ---",
            f"Current Balance: ₹{self.balance}",
            "Transactions:"
        ]

        for txn in self.transactions:
            if start_date and txn.timestamp < start_date:
                continue
            if end_date and txn.timestamp > end_date:
                continue

            statement_lines.append(
                f"{txn.timestamp} | {txn.type.value.upper():12} | Amount: ₹{txn.amount} | "
                f"Balance After: ₹{txn.balance_after} | {txn.description}"
            )

        return "\n".join(statement_lines)


# ------------------------------- Savings Account -------------------------------
class SavingsAccount(Account):
    INTEREST_RATE = Decimal("0.02")  # 2% annual

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        self._record_transaction(TransactionType.WITHDRAWAL, amount, "Savings withdrawal")
        return True

    def calculate_interest(self) -> Decimal:
        interest = self._balance * (self.INTEREST_RATE / 12)  # monthly interest
        self._balance += interest
        self._record_transaction(TransactionType.INTEREST, interest, "Monthly interest")
        return interest


# ------------------------------- Checking Account -------------------------------
class CheckingAccount(Account):
    OVERDRAFT_LIMIT = Decimal("500")
    OVERDRAFT_FEE = Decimal("35")

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0:
            return False

        if self._balance >= amount:
            # Normal withdrawal
            self._balance -= amount
            self._record_transaction(TransactionType.WITHDRAWAL, amount, "Checking withdrawal")
            return True

        # Overdraft case
        overdraft_needed = amount - self._balance
        if overdraft_needed <= self.OVERDRAFT_LIMIT:
            self._balance -= amount
            self._balance -= self.OVERDRAFT_FEE
            self._record_transaction(TransactionType.WITHDRAWAL, amount, "Overdraft withdrawal")
            self._record_transaction(TransactionType.FEE, self.OVERDRAFT_FEE, "Overdraft fee")
            return True

        return False

    def calculate_interest(self) -> Decimal:
        return Decimal("0")  # Checking accounts do not earn interest


# ------------------------------- Business Account -------------------------------
class BusinessAccount(Account):
    INTEREST_RATE = Decimal("0.01")  # 1% annual

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        self._record_transaction(TransactionType.WITHDRAWAL, amount, "Business withdrawal")
        return True

    def calculate_interest(self) -> Decimal:
        interest = self._balance * (self.INTEREST_RATE / 12)
        self._balance += interest
        self._record_transaction(TransactionType.INTEREST,interest, "Business monthly interest")
        return interest


# ------------------------------- Bank Class -------------------------------
class Bank:
    def __init__(self, name: str):
        self.name = name
        self.accounts: dict[str, Account] = {}
        self._next_acc_number = 1001

    def _generate_account_number(self) -> str:
        acc = str(self._next_acc_number)
        self._next_acc_number += 1
        return acc

    def create_account(self, account_type: str, owner: str,
                       initial_deposit: Decimal = Decimal("0")) -> Account:

        acc_no = self._generate_account_number()

        account_type = account_type.lower()
        if account_type == "savings":
            account = SavingsAccount(acc_no, owner, initial_deposit)
        elif account_type == "checking":
            account = CheckingAccount(acc_no, owner, initial_deposit)
        elif account_type == "business":
            account = BusinessAccount(acc_no, owner, initial_deposit)
        else:
            raise ValueError("Invalid account type")

        self.accounts[acc_no] = account
        return account

    def transfer(self, from_account: str, to_account: str,
                 amount: Decimal) -> bool:

        if from_account not in self.accounts or to_account not in self.accounts:
            return False

        sender = self.accounts[from_account]
        receiver = self.accounts[to_account]

        if sender.withdraw(amount):
            receiver.deposit(amount, f"Transfer from {from_account}")
            sender._record_transaction(TransactionType.TRANSFER_OUT, amount,
                                      f"Transfer to {to_account}")
            receiver._record_transaction(TransactionType.TRANSFER_IN, amount,
                                        f"Transfer from {from_account}")
            return True

        return False

    def apply_monthly_interest(self) -> None:
        for acc in self.accounts.values():
            acc.calculate_interest()




def demo():
    print("\n========== BANK SYSTEM DEMO ==========\n")

    # Create a bank
    bank = Bank("Demo National Bank")

    # Create accounts
    savings = bank.create_account("savings", "Suraj", Decimal("1000"))
    checking = bank.create_account("checking", "Suraj", Decimal("500"))
    business = bank.create_account("business", "AutomationsX Pvt Ltd", Decimal("5000"))

    print("Created Accounts:")
    print(f"Savings Account: {savings.account_number}")
    print(f"Checking Account: {checking.account_number}")
    print(f"Business Account: {business.account_number}\n")

    # --- Deposits ---
    savings.deposit(Decimal("500"), "Monthly deposit")
    checking.deposit(Decimal("200"), "Salary credit")
    business.deposit(Decimal("1500"), "Client payment")

    # --- Withdrawals ---
    savings.withdraw(Decimal("300"))
    business.withdraw(Decimal("1000"))

    # --- Overdraft Check ---
    print("\nAttempting Checking Overdraft of ₹900...")
    success = checking.withdraw(Decimal("900"))
    print("Overdraft Success?" , success)
    print("Checking Balance:", checking.balance, "\n")

    # --- Transfer ---
    print("Transferring ₹200 from Savings -> Checking...")
    bank.transfer(savings.account_number, checking.account_number, Decimal("200"))
    print("Savings Balance:", savings.balance)
    print("Checking Balance:", checking.balance, "\n")

    # --- Apply Monthly Interest ---
    print("Applying Monthly Interest...\n")
    bank.apply_monthly_interest()

    print("Updated Balances After Interest:")
    print("Savings:", savings.balance)
    print("Checking:", checking.balance)
    print("Business:", business.balance, "\n")

    # --- Generate Statements ---
    print("\n=== Savings Account Statement ===")
    print(savings.get_statement())

    print("\n=== Checking Account Statement ===")
    print(checking.get_statement())

    print("\n=== Business Account Statement ===")
    print(business.get_statement())

    print("\n========== DEMO COMPLETE ==========")


# Run demo
if __name__ == "__main__":
    demo()

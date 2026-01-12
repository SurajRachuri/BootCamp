from models import Bank
import operations as op


def menu():
    bank = Bank()

    while True:
        print("""
1. Create Account
2. Deposit
3. Withdraw
4. Transfer
5. Statement
6. Exit
""")
        c = input("Choose: ")

        if c == "1":
            op.create_account(bank)
        elif c == "2":
            op.deposit(bank)
        elif c == "3":
            op.withdraw(bank)
        elif c == "4":
            op.transfer(bank)
        elif c == "5":
            op.statement(bank)
        elif c == "6":
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()

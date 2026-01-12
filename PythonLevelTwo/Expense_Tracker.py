# Build a complete expense tracker
# Requirements:
# - Add expenses (amount, category, date, description)
# - View all expenses
# - Filter by category or date range
# - Calculate totals by category
# - Save/load from JSON file
# - Generate monthly summary report


from datetime import datetime
import json
import os


class ExpenseTracker:
    def __init__(self, data_file: str = "expenses.json"):
        self.data_file = data_file
        self.expenses = []
        self.load()

    # ---------------------------------------------------------------
    def add_expense(self, amount: float, category: str,
                    description: str = "", date: str = None) -> dict:
        """Add new expense and return it."""
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        expense = {
            "amount": amount,
            "category": category,
            "date": date,
            "description": description
        }

        self.expenses.append(expense)
        self.save()
        return expense

    # ---------------------------------------------------------------
    def get_expenses(self, category: str = None,
                     start_date: str = None, end_date: str = None) -> list:
        """Get filtered expenses."""

        filtered = self.expenses

        # Filter by category
        if category:
            filtered = [
                e for e in filtered 
                if e["category"].lower() == category.lower()
            ]

        # Safe date parser
        def to_date(d):
            try:
                return datetime.strptime(d, "%Y-%m-%d")
            except:
                return None

        # Filter by start date
        if start_date:
            start = to_date(start_date)
            filtered = [
                e for e in filtered
                if to_date(e["date"]) and to_date(e["date"]) >= start
            ]

        # Filter by end date
        if end_date:
            end = to_date(end_date)
            filtered = [
                e for e in filtered
                if to_date(e["date"]) and to_date(e["date"]) <= end
            ]

        return filtered

    # ---------------------------------------------------------------
    def get_summary(self, month: int = None, year: int = None) -> dict:
        """Calculate totals by category. Supports monthly summary."""

        summary = {}

        for exp in self.expenses:
            try:
                exp_date = datetime.strptime(exp["date"], "%Y-%m-%d")
            except:
                continue  # skip invalid dates

            if month and exp_date.month != month:
                continue

            if year and exp_date.year != year:
                continue

            category = exp["category"]
            summary[category] = summary.get(category, 0) + exp["amount"]

        return summary

    # ---------------------------------------------------------------
    def save(self) -> None:
        """Save all expenses to JSON."""
        with open(self.data_file, "w") as f:
            json.dump(self.expenses, f, indent=4)

    # ---------------------------------------------------------------
    def load(self) -> None:
        """Load expenses from JSON file safely."""

        # If file doesn't exist
        if not os.path.exists(self.data_file):
            self.expenses = []
            return

        try:
            with open(self.data_file, "r") as f:
                content = f.read().strip()

                # Empty file
                if not content:
                    self.expenses = []
                    return

                # Load valid JSON
                self.expenses = json.loads(content)

        except json.JSONDecodeError:
            print("Warning: expenses.json is corrupted! Resetting file.")
            self.expenses = []



# ---------------------------------------------------------------
# TESTING (You can remove this later)

tracker = ExpenseTracker()

tracker.add_expense(250, "Food", "KFC lunch")
tracker.add_expense(1200, "Transport", "Cab to office", "2025-01-05")
tracker.add_expense(500, "Food", "Dominos", "2025/01/12")

print("\n--- Expenses ---")
Expenses=tracker.get_expenses(category="Food")
for i in Expenses:
    for j,k in (i.items()):
        print(f'{j}:{k}') 
    print("----------------------")    

print("\n--- Date Filtered (01 Jan - 10 Jan 2025) ---")
print(tracker.get_expenses(start_date="2025-01-01", end_date="2025-01-10"))

print("\n--- Summary for Jan 2025 ---")
print(tracker.get_summary(month=1, year=2025))

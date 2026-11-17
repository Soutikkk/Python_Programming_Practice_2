
import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


def load_expenses():
    expenses = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                expenses.append(row)

    return expenses


def save_expense(expense):
    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        fields = ["Date", "Category", "Amount", "Description"]
        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists or os.path.getsize(FILE_NAME) == 0:
            writer.writeheader()

        writer.writerow(expense)


def add_expense():
    print("\n--- Add New Expense ---")

    category = input("Enter category (Food/Travel/Shopping/Other): ").strip()
    description = input("Enter description: ").strip()

    try:
        amount = float(input("Enter amount (Rs.): "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

    except ValueError:
        print("Invalid amount! Please enter a number.")
        return

    expense = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Category": category or "Other",
        "Amount": f"{amount:.2f}",
        "Description": description
    }

    save_expense(expense)
    print("Expense added successfully!")


def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    print("-" * 75)
    print(f"{'Date':<18} {'Category':<15} {'Amount':<12} Description")
    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense['Date']:<18} "
            f"{expense['Category']:<15} "
            f"Rs.{float(expense['Amount']):<9.2f} "
            f"{expense['Description']}"
        )


def expense_summary():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available.")
        return

    total = 0
    categories = {}

    for expense in expenses:
        amount = float(expense["Amount"])
        category = expense["Category"]

        total += amount
        categories[category] = categories.get(category, 0) + amount

    print("\n--- Expense Summary ---")
    print(f"Total Spending: Rs.{total:.2f}")

    print("\nCategory-wise Spending:")

    for category, amount in sorted(
        categories.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"{category}: Rs.{amount:.2f}")


def highest_expense():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available.")
        return

    highest = max(expenses, key=lambda x: float(x["Amount"]))

    print("\n--- Highest Expense ---")
    print(f"Date: {highest['Date']}")
    print(f"Category: {highest['Category']}")
    print(f"Amount: Rs.{float(highest['Amount']):.2f}")
    print(f"Description: {highest['Description']}")


def main():
    while True:
        print("\n" + "=" * 40)
        print("       SMART EXPENSE TRACKER")
        print("=" * 40)
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Expense Summary")
        print("4. Highest Expense")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            expense_summary()
        elif choice == "4":
            highest_expense()
        elif choice == "5":
            print("\nThank you for using Smart Expense Tracker!")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()

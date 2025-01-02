import csv
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to the csv file')
    return parser.parse_args()


def read_csv(path):
    transactions = []

    with open(path, 'r', encoding='utf-16') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)

    return transactions


def calculate_expense_for_category(transactions):
    """Calculate total revenues and expenses for each category."""
    revenues, expenses = {}, {}

    for transaction in transactions:
        category = transaction['Category']
        try:
            amount = float(transaction['Amount'])
        except ValueError:
            amount = float(transaction['Amount'].replace(',', ''))

        if transaction['Type'] == 'INCOME':
            revenues[category] = revenues.get(category, 0) + amount
        else:
            expenses[category] = expenses.get(category, 0) + amount
    
    return revenues, expenses


def print_totals(revenues, expenses):
    for category, amount in revenues.items():
        print(f"{category}: {amount:.2f}")
    print()
    for category, amount in expenses.items():
        print(f"{category}: {amount:.2f}")


def fix_names(revenues, expenses):
    categories_to_change = []

    # Add category_in to revenues if category is in expenses
    for category in expenses:
        if category in revenues:
            revenues[f"{category}_in"] = revenues.pop(category)
            categories_to_change.append(category)

    # Add category_out to expenses if category is in revenues
    for category in categories_to_change:
        expenses[f"{category}_out"] = expenses.pop(category)


def create_report(revenues, expenses):
    # Print revenues
    for category, amount in sorted(revenues.items(), key=lambda x: x[1], reverse=True):
        print(f"{category} [{amount:.2f}] Revenues")

    print()
    # Print expenses
    for category, amount in sorted(expenses.items(), key=lambda x: x[1], reverse=True):
        print(f"Revenues [{amount:.2f}] {category}")

    # Calculate and print savings
    savings = sum(revenues.values()) - sum(expenses.values())
    print(f"Revenues [{savings:.2f}] Savings")


def main():
    args = parse_args()
    transactions = read_csv(args.input)
    revenues, expenses = calculate_expense_for_category(transactions)
    # print_totals(revenues, expenses)
    fix_names(revenues, expenses)
    create_report(revenues, expenses)


if __name__ == "__main__":
    main()

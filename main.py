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


def main():
    args = parse_args()
    transactions = read_csv(args.input)
    revenues, expenses = calculate_expense_for_category(transactions)

    for category, amount in revenues.items():
        print(f"{category}: {amount}")
    print()
    for category, amount in expenses.items():
        print(f"{category}: {amount}")


if __name__ == "__main__":
    main()

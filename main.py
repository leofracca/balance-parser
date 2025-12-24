import csv
import argparse
import random
import plotly.graph_objects as go
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=Path, required=True, help='Path to the csv file')
    return parser.parse_args()


def read_csv(path: Path) -> list:
    transactions = []

    with open(path, 'r', encoding='utf-16') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)

    return transactions


def calculate_revenue_and_expense_for_category(transactions: list) -> tuple[dict, dict]:
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


def fix_names(revenues: dict, expenses: dict):
    categories_to_change = []

    # Add category_in to revenues if category is in expenses
    for category in expenses:
        if category in revenues:
            revenues[f"{category}_in"] = revenues.pop(category)
            categories_to_change.append(category)

    # Add category_out to expenses if category is in revenues
    for category in categories_to_change:
        expenses[f"{category}_out"] = expenses.pop(category)


def create_report(revenues: dict, expenses: dict):
    # Print revenues
    for category, amount in sorted(revenues.items(), key=lambda x: x[1], reverse=True):
        print(f"{category} [{amount:.2f}] Revenues")

    print()
    # Print expenses
    for category, amount in sorted(expenses.items(), key=lambda x: x[1], reverse=True):
        print(f"Revenues [{amount:.2f}] {category}")

    # Calculate savings
    savings = sum(revenues.values()) - sum(expenses.values())
    if savings > 0:
        print(f"Revenues [{savings:.2f}] Savings")


def create_sankey_diagram(revenues: dict, expenses: dict, input_file: Path):
    source = [i for i in range(len(revenues.keys()))]
    target = [i + len(revenues) + 1 for i in range(len(expenses.keys()))]

    len_start = len(source)
    rev = [len(source) for _ in range(len(revenues.keys()))]
    for _ in range(len(expenses.keys())):
        source.append(len_start)
    target = rev + target
    value = [amount for amount in revenues.values()] + [amount for amount in expenses.values()]
    # Create a list with all the keys
    labels = list(revenues.keys()) + ["Revenues"] + list(expenses.keys())

    savings = sum(revenues.values()) - sum(expenses.values())
    if savings > 0:
        source.append(len_start)
        target.append(len(labels))
        value.append(savings)
        labels.append("Savings")

    assert len(source) == len(target) == len(value), "Source, target and value lists must have the same length"

    # Build node amounts list
    node_amounts = list(revenues.values()) + [sum(revenues.values())] + list(expenses.values())
    if savings > 0:
        node_amounts.append(savings)
    
    # Set colors for nodes and links
    node_colors = []
    for _ in range(len(labels)):
        node_colors.append(f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.7)")
    
    link_colors = []
    for nc in node_colors:
        link_colors.append(nc.replace(f", 0.7)", ", 0.25)"))
    # Remove revenues node color from link colors
    link_colors = link_colors[:len(revenues)] + link_colors[len(revenues)+1:]

    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 35,
      thickness = 25,
      label = [f"{cat} [{amt:.2f}]" for cat, amt in zip(labels, node_amounts)],
      color = node_colors
    ),
    link = dict(
      source = source,
      target = target,
      value = value,
      color = link_colors
    ))])

    fig.update_layout(title_text=f"{input_file.stem} Sankey Diagram", font_size=25)
    fig.show()


def main():
    args = parse_args()
    transactions = read_csv(args.input)
    revenues, expenses = calculate_revenue_and_expense_for_category(transactions)
    # print_totals(revenues, expenses)
    fix_names(revenues, expenses)
    create_report(revenues, expenses)
    create_sankey_diagram(revenues, expenses, args.input)


if __name__ == "__main__":
    main()

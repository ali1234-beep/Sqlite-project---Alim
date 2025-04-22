import SiegeDatabase
import csv
from datetime import datetime


class R6CreditManager:
    MENU_PROMPT = """
    Please select one of the following options:

    1. Add a new R6 credit transaction. ➕
    2. See all R6 credit transactions. 📜
    3. Find a transaction by operator name. 🔍
    4. See the operator with the highest credit spend. 💵
    5. See total credits spent. 💰
    6. Delete a transaction by name or ID. 👌
    7. Export transactions to CSV. 📧
    8. Import transactions from CSV. 📥
    9. Clear all transactions. 🗑️
    10. EXIT. ❌

    
    Please enter the number of your selection:
    """

    def __init__(self):
        self.connection = SiegeDatabase.connect()
        SiegeDatabase.create_tables(self.connection)

    def run(self):
        while (user_input := input(self.MENU_PROMPT)) != "10":
            if user_input == "1":
                self.add_credit_transaction()
            elif user_input == "2":
                self.view_all_transactions()
            elif user_input == "3":
                self.find_transaction_by_operator()
            elif user_input == "4":
                self.highest_credit_spender()
            elif user_input == "5":
                self.total_credits_spent()
            elif user_input == "6":
                self.delete_transaction()
            elif user_input == "7":
                self.export_transactions_to_csv()
            elif user_input == "8":
                self.import_transactions_from_csv()
            elif user_input == "9":
                self.clear_all_transactions()
            elif user_input == "10":
                self.clear_all_transactions()
            else:
                print("Invalid selection. Please try again.")

    def add_credit_transaction(self):
        operator = input("Enter the operator's name: ")
        item = input("Enter the item purchased (e.g., skin, charm, pack): ")

        while True:
            try:
                amount = int(input("Enter the amount of credits spent: "))
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value for the amount.")

        SiegeDatabase.add_transaction(self.connection, operator, item, amount)
        print(f"Transaction added for operator '{operator}'.")

    def view_all_transactions(self):
        transactions = SiegeDatabase.get_all_transactions(self.connection)
        if transactions:
            print("\nAll Transactions:")
            for transaction in transactions:
                print(f"ID: {transaction[0]}, Operator: {transaction[1]}, Item: {transaction[2]}, Amount: {transaction[3]} credits")
        else:
            print("No transactions found.")

    def find_transaction_by_operator(self):
        operator = input("Enter the operator's name: ")
        transactions = SiegeDatabase.get_transactions_by_operator(self.connection, operator)

        if transactions:
            print(f"\nTransactions for operator '{operator}':")
            for transaction in transactions:
                print(f"ID: {transaction[0]}, Item: {transaction[2]}, Amount: {transaction[3]} credits")
        else:
            print(f"No transactions found for operator '{operator}'.")

    def highest_credit_spender(self):
        operator = input("Enter the operator's name: ")
        spender = SiegeDatabase.get_highest_spender(self.connection, operator)

        if spender:
            print(f"The highest credit spend for operator {operator} is: {spender[2]} credits.")
        else:
            print(f"No transactions found for operator '{operator}'.")

    def total_credits_spent(self):
        total = SiegeDatabase.get_total_credits(self.connection)
        print(f"The total credits spent across all transactions is: {total[0]} credits.")

    def delete_transaction(self):
        delete_choice = input("Would you like to delete by (1) Name or (2) ID? Enter 1 or 2: ")
        if delete_choice == "1":
            name = input("Enter the name of the operator to delete transactions for: ")
            SiegeDatabase.delete_transaction_by_name(self.connection, name)
            print(f"Transactions for operator '{name}' have been deleted.")
        elif delete_choice == "2":
            try:
                transaction_id = int(input("Enter the ID of the transaction to delete: "))
                SiegeDatabase.delete_transaction_by_id(self.connection, transaction_id)
                print(f"Transaction with ID '{transaction_id}' has been deleted.")
            except ValueError:
                print("Invalid input. Please enter a numeric value for the transaction ID.")
        else:
            print("Invalid choice. Returning to the main menu.")

    def export_transactions_to_csv(self):
        transactions = SiegeDatabase.get_all_transactions(self.connection)
        if transactions:
            filename = input("Enter the filename for the exported CSV (without extension): ") + ".csv"
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Operator", "Item", "Amount", "Timestamp"])
                for transaction in transactions:
                    writer.writerow([*transaction, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            print(f"Transactions exported to {filename}.")
        else:
            print("No transactions to export.")

    def import_transactions_from_csv(self):
        filename = input("Enter the filename of the CSV to import: ")
        try:
            with open(filename, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    operator, item, amount = row[1], row[2], int(row[3])
                    SiegeDatabase.add_transaction(self.connection, operator, item, amount)
            print(f"Transactions imported from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"An error occurred while importing: {e}")

    def clear_all_transactions(self):
        confirmation = input("Are you sure you want to delete all transactions? This action cannot be undone. (yes/no): ").strip().lower()
        if confirmation == "yes":
            clear_all_transactions(self.connection)
            print("All transactions have been deleted.")
        else:
            print("Operation canceled.")


def clear_all_transactions(connection):
    with connection:
        connection.execute("DELETE FROM credits;")


if __name__ == "__main__":
    manager = R6CreditManager()
    manager.run()

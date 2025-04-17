import database


class R6CreditManager:
    MENU_PROMPT = """
    Please select one of the following options:

    1. Add a new R6 credit transaction. ➕
    2. See all R6 credit transactions. 📜
    3. Find a transaction by operator name. 🔍
    4. See the operator with the highest credit spend. 💵
    5. See total credits spent. 💰
    6. Delete a transaction by name or ID. 👌
    7. EXIT. ❌

    Your selection: 
    """

    def __init__(self):
        self.connection = database.connect()
        database.create_tables(self.connection)

    def run(self):
        while (user_input := input(self.MENU_PROMPT)) != "7":
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

        database.add_transaction(self.connection, operator, item, amount)
        print(f"Transaction added for operator '{operator}'.")

    def view_all_transactions(self):
        transactions = database.get_all_transactions(self.connection)
        if transactions:
            print("\nAll Transactions:")
            for transaction in transactions:
                print(f"ID: {transaction[0]}, Operator: {transaction[1]}, Item: {transaction[2]}, Amount: {transaction[3]} credits")
        else:
            print("No transactions found.")

    def find_transaction_by_operator(self):
        operator = input("Enter the operator's name: ")
        transactions = database.get_transactions_by_operator(self.connection)

        if transactions:
            print(f"\nTransactions for operator '{operator}':")
            for transaction in transactions:
                print(f"ID: {transaction[0]}, Item: {transaction[2]}, Amount: {transaction[3]} credits")
        else:
            print(f"No transactions found for operator '{operator}'.")

    def highest_credit_spender(self):
        operator = input("Enter the operator's name: ")
        spender = database.get_highest_spender(self.connection, operator)

        if spender:
            print(f"The highest credit spend for operator {operator} is: {spender[2]} credits.")
        else:
            print(f"No transactions found for operator '{operator}'.")

    def total_credits_spent(self):
        total = database.get_total_credits(self.connection)
        print(f"The total credits spent across all transactions is: {total[0]} credits.")

    def delete_transaction(self):
        delete_choice = input("Would you like to delete by (1) Name or (2) ID? Enter 1 or 2: ")
        if delete_choice == "1":
            name = input("Enter the name of the operator to delete transactions for: ")
            database.delete_transaction_by_name(self.connection, name)
            print(f"Transactions for operator '{name}' have been deleted.")
        elif delete_choice == "2":
            try:
                transaction_id = int(input("Enter the ID of the transaction to delete: "))
                database.delete_transaction_by_id(self.connection, transaction_id)
                print(f"Transaction with ID '{transaction_id}' has been deleted.")
            except ValueError:
                print("Invalid input. Please enter a numeric value for the transaction ID.")
        else:
            print("Invalid choice. Returning to the main menu.")


if __name__ == "__main__":
    manager = R6CreditManager()
    manager.run()

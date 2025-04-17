import database

MENU_PROMPT = """

Please select one of the following options:

1. Add a new R6 credit transaction.
2. See all R6 credit transactions.
3. Find a transaction by operator name.
4. See the operator with the highest credit spend.
5. See total credits spent.
6. Delete a transaction by name or ID.
7. EXIT.

Your selection: 

"""

GET_HIGHEST_SPENDER = """
SELECT * FROM credits
WHERE operator = ? AND amount = (SELECT MAX(amount) FROM credits WHERE operator = ?)
"""

GET_TOTAL_CREDITS = """
SELECT SUM(amount) FROM credits
"""

def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "7":
        if user_input == "1":
            add_credit_transaction(connection)
           
        elif user_input == "2":
            view_all_transactions(connection)

        elif user_input == "3":
            find_transaction_by_operator(connection)

        elif user_input == "4":
            highest_credit_spender(connection)

        elif user_input == "5":
            total_credits_spent(connection)

        elif user_input == "6":
            delete_transaction(connection)
  
        else:
            print("Invalid selection. Please try again.")

def delete_transaction(connection):
    delete_choice = input("Would you like to delete by (1) Name or (2) ID? Enter 1 or 2: ")
    if delete_choice == "1":
        name = input("Enter the name of the operator to delete transactions for: ")
        database.delete_transaction_by_name(connection, name)
        print(f"Transactions for operator '{name}' have been deleted.")
    elif delete_choice == "2":
        transaction_id = int(input("Enter the ID of the transaction to delete: "))
        database.delete_transaction_by_id(connection, transaction_id)
        print(f"Transaction with ID '{transaction_id}' has been deleted.")
    else:
        print("Invalid choice. Returning to the main menu.")

def highest_credit_spender(connection):
    operator = input("Enter the operator's name: ")
    spender = database.get_highest_spender(connection, operator)

    print(f"The highest credit spend for operator {operator} is: {spender[2]} credits.")

def total_credits_spent(connection):
    total = database.get_total_credits(connection)
    print(f"The total credits spent across all transactions is: {total[0]} credits.")

def find_transaction_by_operator(connection):
    operator = input("Enter the operator's name: ")
    transactions = database.get_transactions_by_operator(connection, operator)  # Pass operator here

    for transaction in transactions:
        print(f"Operator: {transaction[1]}, Item: {transaction[2]}, Amount: {transaction[3]} credits")

def view_all_transactions(connection):
    transactions = database.get_all_transactions(connection)

    for transaction in transactions:
        print(f"Operator: {transaction[1]}, Item: {transaction[2]}, Amount: {transaction[3]} credits")

def add_credit_transaction(connection):
    operator = input("Enter the operator's name: ")
    item = input("Enter the item purchased (e.g., skin, charm, pack): ")
    
    while True:
        try:
            amount = int(input("Enter the amount of credits spent: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the amount.")

    database.add_transaction(connection, operator, item, amount)

menu()

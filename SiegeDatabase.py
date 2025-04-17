import sqlite3
CREATE_SIEGE_TABLE = "Create Table IF NOT EXISTS siege (id INTEGER PRIMARY KEY, name TEXT, method text, Rating integer);"

INSERT_SIEGE = "INSERT INTO siege (name, method, rating) VALUES (?, ?, ?);"

GET_ALL_SIEGE = "SELECT * FROM siege;"
GET_SIEGE_BY_NAME = "SELECT * FROM siege WHERE name = ?;"
GET_BEST_PREPARATION_FOR_SIEGE = """
SELECT * FROM siege
WHERE name = ? AND rating = (SELECT MAX(rating) FROM siege WHERE name = ?)
LIMIT 1;"""

CREATE_OPERATORS_TABLE = "CREATE TABLE IF NOT EXISTS operators (id INTEGER PRIMARY KEY, name TEXT, method TEXT, rating INTEGER);"

INSERT_OPERATOR = "INSERT INTO operators (name, method, rating) VALUES (?, ?, ?);"

GET_ALL_OPERATORS = "SELECT * FROM operators;"
GET_OPERATOR_BY_NAME = "SELECT * FROM operators WHERE name = ?;"
GET_BEST_PREPARATION_FOR_OPERATOR = """
SELECT * FROM operators
WHERE name = ? AND rating = (SELECT MAX(rating) FROM operators WHERE name = ?)
LIMIT 1;
"""

CREATE_CREDITS_TABLE = """
CREATE TABLE IF NOT EXISTS credits (
    id INTEGER PRIMARY KEY,
    operator TEXT,
    item TEXT,
    amount INTEGER
);
"""

INSERT_TRANSACTION = "INSERT INTO credits (operator, item, amount) VALUES (?, ?, ?);"

GET_ALL_TRANSACTIONS = "SELECT * FROM credits;"
GET_TRANSACTIONS_BY_OPERATOR = "SELECT * FROM credits WHERE operator = ?;"
GET_HIGHEST_SPENDER = """
SELECT * FROM credits
WHERE operator = ? AND amount = (SELECT MAX(amount) FROM credits WHERE operator = ?)
LIMIT 1;
"""
GET_TOTAL_CREDITS = "SELECT SUM(amount) FROM credits;"

DELETE_TRANSACTION_BY_NAME = "DELETE FROM credits WHERE operator = ?;"
DELETE_TRANSACTION_BY_ID = "DELETE FROM credits WHERE id = ?;"


def connect():
    return sqlite3.connect("data.db")


def create_tables(connection):
    with connection: 
        connection.execute(CREATE_SIEGE_TABLE)
        connection.execute(CREATE_CREDITS_TABLE)
        connection.execute(CREATE_OPERATORS_TABLE)

def add_bean(connection, name, method, rating):
    with connection:
        connection.execute(INSERT_SIEGE, (name, method, rating))

def get_all_beans(connection):
    with connection:
        return connection.execute(GET_ALL_SIEGE).fetchall()

def get_beans_by_name(connection, name):
    with connection:
        return connection.execute(GET_SIEGE_BY_NAME, (name,)).fetchall()
    
def get_best_preparation_for_bean(connection, name):
    return connection.execute(GET_BEST_PREPARATION_FOR_SIEGE, (name, name)).fetchone()

def add_transaction(connection, operator, item, amount):
    with connection:
        connection.execute(INSERT_TRANSACTION, (operator, item, amount))


def get_all_transactions(connection):
    with connection:
        return connection.execute(GET_ALL_TRANSACTIONS).fetchall()


def get_transactions_by_operator(connection, operator):
    with connection:
        return connection.execute(GET_TRANSACTIONS_BY_OPERATOR, (operator,)).fetchall()


def get_highest_spender(connection, operator):
    return connection.execute(GET_HIGHEST_SPENDER, (operator, operator)).fetchone()


def get_total_credits(connection):
    with connection:
        return connection.execute(GET_TOTAL_CREDITS).fetchone()


def delete_transaction_by_name(connection, operator):
    with connection:
        connection.execute(DELETE_TRANSACTION_BY_NAME, (operator,))


def delete_transaction_by_id(connection, transaction_id):
    with connection:
        connection.execute(DELETE_TRANSACTION_BY_ID, (transaction_id,))

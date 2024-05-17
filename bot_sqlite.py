import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

def create_users():
    command = """CREATE TABLE IF NOT EXISTS USERS (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    full_name VARCHAR(40),
    first_name VARCHAR(40),
    last_name VARCHAR(40),
    age INTEGER,
    region VARCHAR(40),
    phone_number INTEGER
    )"""
    cursor.execute(command)
    connection.commit()

def add_user(telegram_id, full_name):
    command = """INSERT INTO USERS (telegram_id, full_name) 
                 VALUES (?, ?)"""
 
    cursor.execute(command, (telegram_id, full_name))
    connection.commit()  

def add_user_full(first_name, last_name, age, region, phone_number,telegram_id):
    command = f"""Update USERS set first_name=?, last_name=?, age=?, region=?, phone_number=? 
                 where telegram_id=?"""

    cursor.execute(command, (first_name, last_name, age, region, phone_number,telegram_id))
    connection.commit()
    

def count_users():
    command = """SELECT count(*) FROM USERS"""
    cursor.execute(command)
    return cursor.fetchone()

def get_all_user_ids():
    command = """SELECT telegram_id FROM USERS"""
    cursor.execute(command)
    return cursor.fetchall()
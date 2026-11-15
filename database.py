from dotenv import load_dotenv
import psycopg
import os
import werkzeug.security
load_dotenv()

def db_sync():
    connection = psycopg.connect(os.getenv("postgr_login"))
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE CHECK(length(email) <=254),  
                    password TEXT NOT NULL,
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL)""") # checks if email is within internet legal limit and not duplicate or empty
    connection.commit()
    return cursor, connection

def check_login(email, cursor, connection):
    cursor.execute("""SELECT password FROM users WHERE email = %s""",(email,))
    result = cursor.fetchone()
    if result == None: # if there's no password for the email used
        return False
    else:
        return result[0]

def create_account(details):
    connection = psycopg.connect(os.getenv("postgr_login"))
    first, last, email, password = details
    new_pass = werkzeug.security.generate_password_hash(password)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (email, password, firstName, lastName) VALUES (%s, %s, %s, %s)", (email, new_pass, first, last))
    connection.commit()
    return True

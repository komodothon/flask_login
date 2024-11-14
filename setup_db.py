import sqlite3
import uuid
from flask_bcrypt import Bcrypt
from os.path import join

DATABASE = join('instance','users.db')
bcrypt = Bcrypt()


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
                   id TECT PRIMARY KEY,
                   username TEXT UNIQUE NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   password_hash TEXT NOT NULL)
        """)
    
    connection.close()

def add_sample_users():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    for i in range(1,6):
        id = str(uuid.uuid4())
        username = f'user{i}'
        email = f'user{i}@sample.com'
        password = f'Hello{i}'
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        prepped_user_data = (id, username, email, password_hash)
        
        cursor.execute("""
            INSERT INTO users (id, username, email, password_hash) VALUES (?, ?, ?, ?)
            """, prepped_user_data)

    connection.commit()
    connection.close()
        

if __name__ == "__main__":
    init_db()
    add_sample_users()
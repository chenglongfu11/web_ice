import sqlite3

conn = sqlite3.connect('users.sqlite3')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE user(name,age,phone)
'''
)

cursor.execute('''
    INSERT INTO user(name,age,phone)
    value ('Clong',18,'1292992')
'''
)

cursor.execute(
    'SELECT * from user'
)

for item in cursor.fetchall():\
    print(item)
import sqlite3

connection = sqlite3.connect('my_data.db')

cursor = connection.cursor()

# Drop table if exists and create new table here
drop_if_exists = "DROP TABLE IF EXISTS users"
cursor.execute(drop_if_exists)
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

# Single INSERT query
user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES(?, ?, ?)"
cursor.execute(insert_query, user)

# Many INSERT queries
users = [
    (2, 'bob', 'bnm'),
    (3, 'smg4', 'fhjsdkll'),
    (4, 'tari', '75342899'),
    (5, 'meggy', 'ghsjldakak')
]
cursor.executemany(insert_query, users)

# SELECT statement
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
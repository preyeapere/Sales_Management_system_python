#Description: This python script assumes that you already have
# a database.db file at the root of your workspace.
# This python script will CREATE a table called Sales 
# in the database.db using SQLite3 which will be used
# to store the data collected by the forms in this app
# Execute this python script before testing or editing this app code. 
# Open a python terminal and execute this script:
# python new_table.py

import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

conn.execute('CREATE TABLE sales (product_nm TEXT, category TEXT, quantity TEXT, price TEXT)')


print("Created table successfully!")

conn.close()


import csv
import psycopg2

# Database configuration
DATABASE = 'your_database_name'
USER = 'your_username'
PASSWORD = 'your_password'
HOST = 'localhost'
PORT = 5432

# Connect to the PostgreSQL database
conn = psycopg2.connect(database=DATABASE, user=USER,
                        password=PASSWORD, host=HOST, port=PORT)
cursor = conn.cursor()

# Fetch data from the table
cursor.execute("SELECT * FROM your_table_name;")
rows = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]

# Write data to CSV
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(column_names)
    writer.writerows(rows)

cursor.close()
conn.close()

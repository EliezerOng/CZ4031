import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="TPC-H", user='postgres', password='admin123', host='localhost'
)

print("Connecting to sql database...")
cursor = conn.cursor()

print("Executing SQL query")
cursor.execute("SELECT * FROM customer")

print("SQL query executed")
print(cursor.fetchone())




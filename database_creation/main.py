import mysql.connector
from create_tables import create_tables
from add_nodes import add_nodes
from add_events import add_events

# Connect to the database
mydb = mysql.connector.connect(
    host="hogrider-mysql.mysql.database.azure.com",
    user="csce483",
    password="Hogr!ders483",
    database="csce483"
)

create_tables(mydb)
add_nodes(mydb)

# List all nodes in node table
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM nodes")
result = mycursor.fetchall()
print("Nodes in nodes table:")
for row in result:
    print(row)

add_events(mydb)

# Close the database connection
mydb.close()
import mysql.connector
import datetime
import random

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hogr!ders483",
    database="csce483"
)

# Create a cursor object
mycursor = mydb.cursor()

# Create query of randomized data to insert into events table
node_id = 1
# store current time
event_time = datetime.datetime.now()
animal = random.choice(["hawk", "coyote", "hog", "fox"])
video = 'video.mp4'
sql = "INSERT INTO events (node_id, event_time, animal, video) VALUES (%s, %s, %s, %s)"

# Convert the data types of values to match the table columns
values = (node_id, event_time, animal, video)

# Execute the query with the values
mycursor.execute(sql, values)
mydb.commit()

# Close the database connection
mydb.close()
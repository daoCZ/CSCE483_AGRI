import mysql.connector
import datetime
import random
import socket
import time


def check_node(mydb, mycursor):
    # Grab IP address of computer (Linux)
    ip = socket.gethostbyname(socket.gethostname())
    print("IP address of computer: " + ip)

    # Establish node name
    node_name = 'Node 1'

    # Check if node exists in nodes table, if not, add it. If it does exist, update the ip address
    sql = "SELECT * FROM nodes WHERE name = %s"
    val = (node_name,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    if len(result) == 0:
        # Add node to nodes table
        print("Node not in database, adding node to nodes table...")
        sql = "INSERT INTO nodes (name, ip_address) VALUES (%s, %s)"
        val = (node_name, ip)
    else:
        # Update ip address of node
        sql = "UPDATE nodes SET ip_address = %s WHERE name = %s"
        val = (ip, node_name)
    mycursor.execute(sql, val)
    mydb.commit()

    # Find node id of node
    sql = "SELECT node_id FROM nodes WHERE name = %s"
    val = (node_name,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    node_id = result[0][0]
    
    return node_id

def event_sim(node_id, duration, mydb, mycursor):

    # Determine random number of events to print over duration
    num_events = random.randint(5, 15)
    print("Number of events: " + str(num_events))

    # Get time between events
    time_between_events = duration*60/num_events

    # Store current time
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(minutes=duration)

    for i in range(num_events):
        # Check if current time is greater than end time, if it is, break out of loop
        if datetime.datetime.now() > end_time:
            break
        
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
        # Sleep for random time between 0 and time_between_events
        time.sleep(time_between_events)

   
    
def main():
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        # password="Hogr!ders483",
        password="Sillysongs1",
        database="csce483"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    
    node_id = check_node(mydb, mycursor)
    
    # Ask user for duration
    duration = float(input("How long would you like this script to run for (minutes)? "))

    event_sim(node_id, duration, mydb, mycursor)

    # Close the database connection
    print("Closing database connection...")
    try:
        mydb.close()
    except:
        print("Database connection already closed.")
    print("Database connection closed.")

main()

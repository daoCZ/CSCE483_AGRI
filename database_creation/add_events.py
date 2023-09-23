import random
import datetime

def add_events(mydb):
    # Create a cursor object
    mycursor = mydb.cursor()
    
    # Grab list of node ids from node table and store in list
    mycursor.execute("SELECT node_id FROM nodes")
    node_ids = mycursor.fetchall()
    
    # Get input frpm user for number of events to add
    num_events = int(input("How many events would you like to add? "))
    
    # Create list of event times, animal names (hawk, coyote, hog, or fox),  that corresponds with length of node_ids list
    for i in range(num_events):
        node_id = random.choice(node_ids)[0]  # Extract the first element of the tuple
        # Generate random datetime object
        event_time = datetime.datetime.now()+random.random()*datetime.timedelta(days=365)
        animal = random.choice(["hawk", "coyote", "hog", "fox"])
        video = 'video'
        sql = "INSERT INTO events (node_id, event_time, animal, video) VALUES (%s, %s, %s, %s)"
        
        # Convert the data types of values to match the table columns
        values = (node_id, event_time, animal, video)

        # Execute the query with the values
        mycursor.execute(sql, values)
    print("Adding event to events table...")
    
    # Print all events in events table
    mycursor.execute("SELECT * FROM events")
    result = mycursor.fetchall()
    print("Events in events table:")
    for row in result:
        print(row)
    
    
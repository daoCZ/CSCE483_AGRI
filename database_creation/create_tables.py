def create_tables (mydb):
    # Create a cursor object
    mycursor = mydb.cursor()

    mycursor.execute("DROP TABLE IF EXISTS events")
    mycursor.execute("DROP TABLE IF EXISTS nodes")

    # Create list of sql commands to create tables
    create_tables = ["CREATE TABLE nodes (node_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), ip_address VARCHAR(255))",
                    "CREATE TABLE events (event_id INT AUTO_INCREMENT PRIMARY KEY, node_id INT, event_time DATETIME, animal VARCHAR(255), video VARCHAR(255), FOREIGN KEY (node_id) REFERENCES nodes(node_id))"]

    # Execute the sql commands
    for command in create_tables:
        mycursor.execute(command)
        
    print("Tables created!\n")

    # Execute the query to show columns from the nodes table
    mycursor.execute("SHOW COLUMNS FROM nodes")
    result = mycursor.fetchall()
    print("Columns from nodes table:")
    # Print the rows
    for row in result:
        print(row)
        
    print ("\n")
    # Execute the query to show columns from the events table
    mycursor.execute("SHOW COLUMNS FROM events")
    result = mycursor.fetchall()
    print("Columns from events table:")
    # Print the rows
    for row in result:
        print(row)
    

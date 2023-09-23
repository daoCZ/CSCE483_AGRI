def add_nodes(mydb):
    # Create a cursor object
    mycursor = mydb.cursor()
    # Ask user for number of nodes to add
    num_nodes = int(input("How many nodes would you like to add? "))
    
    # Create list of node names
    node_names = []
    while len(node_names) < num_nodes:
        node_names.append("Node " + str(len(node_names)+1))    
    # Add all nodes to the nodes table
    for name in node_names:
        sql = "INSERT INTO nodes (name) VALUES (%s)"
        val = (name,)
        mycursor.execute(sql, val)
        mydb.commit()
    
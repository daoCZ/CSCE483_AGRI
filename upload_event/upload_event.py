import mysql.connector

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(node_id, event_time, animal, video):
    print("Inserting event into events table")
    try:
        connection = mysql.connector.connect(host="localhost",
                                             user="root",
                                             password="Sillysongs1",
                                             database="csce483")

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO events
                          (node_id, event_time, animal, video) VALUES (%s,%s,%s,%s)"""

        file = convertToBinaryData(video)

        # Convert data into tuple format
        insert_blob_tuple = (node_id, event_time, animal, video)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Event successfully added to events table", result)

    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

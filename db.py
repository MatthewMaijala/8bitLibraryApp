# File for handling database connections, queries, and logic for the application.
import mysql.connector

def get_connection():
    """
    Establishes a connection to the MySQL database.
    Returns the connection object.
    """
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mattijala132!", # Please change this to your local MySQL password
    port=3306,
    database="library_db" # Please change this to your local MySQL database name
    )

    print("Connected to the database" if conn.is_connected() else "Failed to connect to the database")
    return conn
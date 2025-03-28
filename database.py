import mysql.connector
from mysql.connector import errorcode

def create_connection():
    """Create a MySQL database connection."""
    # Example configuration dictionary
    # config = {
    #     'user': 'root',
    #     'password': '',
    #     'host': 'localhost',  # or your MySQL server's IP address
    #     'database': 'utility_services_db',
    #     'raise_on_warnings': True
    # }
    config = {
        'user': 'admin',
        'password': 'x24112682-utility-rds',
        'host': 'x24112682-utility-rds.cid6gtv3k6ak.ap-southeast-2.rds.amazonaws.com',  # or your MySQL server's IP address
        'database': 'x24112682-utility-rds',
        'raise_on_warnings': True
    }
    try:
        conn = mysql.connector.connect(**config)
        print("Connection successful.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(f"Error: {err}")
        return None



""" # Use the connection function
conn = create_connection()
if conn:
    cursor = conn.cursor()

    
    cursor.execute(create_table_query)
    print("Table created successfully.")

    # Close the cursor and connection
    cursor.close()
    conn.close() """

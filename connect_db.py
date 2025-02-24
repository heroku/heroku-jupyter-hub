import os
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL']


if __name__ == "__main__":

    db_connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Create a cursor object
    cursor = db_connection.cursor()

    # Query the 'app_config' table for the entry with the key 'PROXY_PORT'
    query = "SELECT value FROM app_config WHERE key = %s;"
    cursor.execute(query, ('PROXY_PORT',))

    # Fetch the result
    result = cursor.fetchone()

    # Check if a value was found
    if result:
        proxy_port = result[0]
        print(f"PROXY_PORT: {proxy_port}")

        # Write value to text file
        with open("proxy_port.txt", "w") as file:
            file.write(proxy_port)
        print("Proxy port value successfully written to file.")

        # Close the cursor and connection
        cursor.close()
        db_connection.close()

        # Exit and return proxy port 
        exit(0)

    else:
        print("PROXY_PORT not found in app_config table.")
        
        # Close the cursor and connection
        cursor.close()
        db_connection.close()

        # Exit with value indicating failure
        exit(1)

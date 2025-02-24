import os
import psycopg2
import time
from psycopg2 import OperationalError

DATABASE_URL = os.environ['DATABASE_URL']
MAX_RETRIES = 5
RETRY_DELAY = 3

def connect_with_retry():
    for attempt in range(MAX_RETRIES):
        try:
            return psycopg2.connect(DATABASE_URL, sslmode='require')
        except OperationalError as e:
            if attempt == MAX_RETRIES - 1:
                raise e
            print(f"Database connection attempt {attempt + 1} failed. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

if __name__ == "__main__":
    try:
        db_connection = connect_with_retry()
        cursor = db_connection.cursor()

        # Just verify we can connect to the database
        cursor.execute("SELECT 1")
        print("Database connection successful")
        exit(0)

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

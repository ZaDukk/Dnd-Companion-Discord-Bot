import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
database_url = os.getenv("DATABASE_URL")

def create_tables():
    """Create necessary tables in the database."""
    try:
        # Connect to the database
        conn = psycopg2.connect(database_url)
        with conn.cursor() as cur:
            # Create the campaigns table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    dm_id BIGINT,
                    players JSONB DEFAULT '[]'
                );
            """)
            conn.commit()
            print("Table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

# Call the function to create tables
if __name__ == "__main__":
    create_tables()
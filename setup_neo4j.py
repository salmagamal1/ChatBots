import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

if not all([uri, username, password]):
    raise ValueError("Missing Neo4j environment variables.")

driver = GraphDatabase.driver(uri, auth=(username, password))

def test_connection():
    try:
        driver.verify_connectivity()
        print("System: Successfully connected to Neo4j!")
    except Exception as e:
        print(f"System: Connection failed: {e}")

def execute_query(query, parameters=None):
    with driver.session() as session:
        # Use .run() and then .data() or .consume()
        result = session.run(query, parameters)
        # For WRITE operations (ADD/UPDATE/DELETE), you must consume the result
        # to ensure the transaction is completed.
        return result.data()


if __name__ == "__main__":
    test_connection()
    driver.close()
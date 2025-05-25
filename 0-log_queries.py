import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """
    Decorator that logs SQL queries with timestamp before executing them.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from either positional or keyword arguments
        query = args[0] if args else kwargs.get('query', '')
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print the query with timestamp
        print(f"[{timestamp}] Executing query: {query}")
        
        try:
            # Execute the original function
            result = func(*args, **kwargs)
            print(f"[{timestamp}] Query executed successfully")
            return result
        except Exception as e:
            print(f"[{timestamp}] Query failed with error: {str(e)}")
            raise
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
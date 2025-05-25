import sqlite3
import functools
import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DB_QUERY_LOGGER")

def log_queries(func):
    """
    Decorator that logs SQL queries before executing them.
    
    Args:
        func: The function to be decorated
        
    Returns:
        A wrapped function that logs the query before execution
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from either positional or keyword arguments
        query = args[0] if args else kwargs.get('query', '')
        
        # Log the query before execution
        logger.info(f"Executing query: {query}")
        
        try:
            # Execute the original function
            result = func(*args, **kwargs)
            logger.info("Query executed successfully")
            return result
        except Exception as e:
            logger.error(f"Query failed with error: {str(e)}")
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
import time
import sqlite3 
import functools

# Global cache dictionary to store query results
query_cache = {}

def with_db_connection(func):
    """
    Decorator that handles database connection automatically.
    Opens connection before execution and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Inject connection if not provided
            if 'conn' not in kwargs and not any(isinstance(arg, sqlite3.Connection) for arg in args):
                kwargs['conn'] = conn
            return func(*args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """
    Decorator that caches database query results based on the query string.
    Subsequent calls with the same query will return the cached result.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from arguments
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        
        if query is None:
            return func(*args, **kwargs)
            
        # Check if query is in cache
        if query in query_cache:
            print(f"Returning cached result for query: {query}")
            return query_cache[query]
            
        # Execute query and cache result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        return result
        
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
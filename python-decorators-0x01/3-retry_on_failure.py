import time
import sqlite3 
import functools

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

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries database operations on failure.
    
    Args:
        retries (int): Number of retry attempts
        delay (int): Delay between retries in seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    last_exception = e
                    if attempt < retries - 1:
                        time.sleep(delay)
                        continue
                    raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
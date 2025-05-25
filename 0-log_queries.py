import sqlite3
import functools
from datetime import datetime  # Required import

# Decorator to log SQL queries
def log_queries(fn):
    @functools.wraps(fn)
    def wrapper(query):
        print(query)
        fn(query)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

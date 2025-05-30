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

def transactional(func):
    """
    Decorator that manages database transactions.
    Commits if successful, rolls back if exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
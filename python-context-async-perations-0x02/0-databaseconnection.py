import sqlite3

class DatabaseConnection:
    """Custom context manager for database connections"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
    
    def __enter__(self):
        """Open the database connection when entering the context"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection when exiting the context"""
        if self.conn:
            self.conn.close()
        # Handle any exceptions that occurred in the with block
        if exc_type is not None:
            print(f"An error occurred: {exc_val}")
        # Return False to propagate exceptions, True to suppress them
        return False

# Using the context manager to query the database
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    
    # Print the query results
    print("User data:")
    for row in results:
        print(row)
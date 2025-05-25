import sqlite3

class ExecuteQuery:
    """Context manager that executes a parameterized query and returns results"""
    
    def __init__(self, db_name, query, params=None):
        """
        Initialize with database name, query, and parameters
        
        Args:
            db_name: Name/path of the SQLite database
            query: SQL query to execute
            params: Parameters for the query (tuple/list/dict)
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """Execute the query when entering the context"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params or ())
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the context"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Return False to propagate any exceptions
        return False

# Example usage
with ExecuteQuery(
    db_name='users.db',
    query="SELECT * FROM users WHERE age > ?",
    params=(25,)
) as results:
    print("Users over 25:")
    for user in results:
        print(user)
import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "issues.db")

def clear_db():
    """Delete all rows from the issues table."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM issues")
    conn.commit()
    conn.close()
    print("All issues cleared from the database.")

if __name__ == "__main__":
    clear_db()
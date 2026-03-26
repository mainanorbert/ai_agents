import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "issues.db")

print(f"Database path: {DB_PATH}")

def init_db(db_path: str = DB_PATH) -> None:
    """Create the issues table if it doesn't already exist."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT NOT NULL,
            command TEXT NOT NULL,
            project_path TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database created at {DB_PATH}")

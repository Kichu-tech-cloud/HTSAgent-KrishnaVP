import sqlite3
import os

# Define the path for the new database
DB_PATH = os.path.join("modules", "hts_data.db")

def initialize_database():
    # Create a connection to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the `documents` table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    # Populate the `documents` table with example data
    data = [
        ("The United States-Israel Free Trade Agreement (FTA) is the first free trade agreement entered into by the United States."),
        ("Signed in 1985, it aims to eliminate trade barriers and promote economic cooperation between the United States and Israel."),
        ("Under the agreement, tariffs on industrial and agricultural goods between the two nations are reduced or eliminated."),
        ("The FTA has provisions to resolve trade disputes and protect intellectual property rights."),
        ("The agreement has significantly increased trade volume, benefiting industries like technology, agriculture, and pharmaceuticals.")
    ]

    cursor.executemany("INSERT INTO documents (content) VALUES (?)", [(d,) for d in data])
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()

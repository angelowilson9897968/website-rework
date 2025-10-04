import sqlite3

# Connect to the existing database
conn = sqlite3.connect('portfolios.db')
cursor = conn.cursor()

# Create the new 'results' table to store user submissions
# This will store the score, the time taken in seconds, and a timestamp
cursor.execute('''
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    risk_score INTEGER NOT NULL,
    time_taken_seconds REAL NOT NULL,
    submission_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit the change and close the connection
conn.commit()
conn.close()

print("✅ 'results' table created successfully or already exists.")
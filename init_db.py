import sqlite3

# SQLite database file
DB_FILE = "user_data.db"


# Initialize database
def init_db2():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            encoding BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def init_db(db_name="licensePlatesDatabase.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LicensePlates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            license_plate TEXT NOT NULL,
            frame_path TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' initialized successfully.")
    
def init_plate_table():
    conn = sqlite3.connect('licensePlatesDatabase.db')
    cursor = conn.cursor()

    # Create table for authorized and blacklisted plates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plates (
            plate_number TEXT PRIMARY KEY,
            list_type TEXT NOT NULL
        )
    ''')

    # Create table for email settings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            smtp_server TEXT,
            smtp_port INTEGER,
            email_address TEXT,
            email_password TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_plate_table()
init_db2()
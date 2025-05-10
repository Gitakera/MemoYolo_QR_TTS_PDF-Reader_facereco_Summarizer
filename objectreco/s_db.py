import sqlite3

# Save data to the LicensePlates table
def save_to_database(data_batch):
    conn = sqlite3.connect('licensePlatesDatabase.db')
    cursor = conn.cursor()

    # Convert dictionaries to tuples
    formatted_data = [
        (entry["start_time"], entry["end_time"], entry["license_plate"], entry["frame_path"])
        for entry in data_batch
    ]

    cursor.executemany('''
        INSERT INTO LicensePlates (start_time, end_time, license_plate, frame_path)
        VALUES (?, ?, ?, ?)
    ''', formatted_data)

    conn.commit()
    conn.close()

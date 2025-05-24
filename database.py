# database.py
import sqlite3
from sqlite3 import Error

DATABASE_NAME = "flights.db"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    try:
        sql_create_reservations_table = """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            flight_number TEXT NOT NULL,
            departure TEXT NOT NULL,
            destination TEXT NOT NULL,
            date TEXT NOT NULL,
            seat_number TEXT NOT NULL
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_reservations_table)
        conn.commit()
    except Error as e:
        print(f"Error creating table: {e}")

def add_reservation(conn, reservation_details):
    sql = ''' INSERT INTO reservations(name, flight_number, departure, destination, date, seat_number)
              VALUES(?,?,?,?,?,?) '''
    cursor = conn.cursor()
    try:
        cursor.execute(sql, reservation_details)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error adding reservation: {e}")
        return None

def get_all_reservations(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM reservations ORDER BY id DESC")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error fetching reservations: {e}")
        return []

def get_reservation_by_id(conn, reservation_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM reservations WHERE id=?", (reservation_id,))
        row = cursor.fetchone()
        return row
    except Error as e:
        print(f"Error fetching reservation by ID: {e}")
        return None

def update_reservation(conn, reservation_id, updated_details):
    sql = ''' UPDATE reservations
              SET name = ? ,
                  flight_number = ? ,
                  departure = ? ,
                  destination = ? ,
                  date = ? ,
                  seat_number = ?
              WHERE id = ?'''
    cursor = conn.cursor()
    try:
        data_to_update = updated_details + (reservation_id,)
        cursor.execute(sql, data_to_update)
        conn.commit()
        return True
    except Error as e:
        print(f"Error updating reservation: {e}")
        return False

def delete_reservation(conn, reservation_id):
    sql = 'DELETE FROM reservations WHERE id=?'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (reservation_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error deleting reservation: {e}")
        return False

def initialize_database():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    initialize_database()
    print(f"Database '{DATABASE_NAME}' initialized.")

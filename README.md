# Simple Flight Reservation Desktop App

Simple Flight Reservation Desktop App By Giovanni! This project is a basic flight reservation system developed as a desktop application using Python's Tkinter library for the Graphical User Interface (GUI) and SQLite for database management. Users can book, view, update, and delete flight reservations.

I hope this application serves as a useful example or a starting point for your own projects!

## Features

* **Book Flights**: Add new flight reservations with passenger details.
* **View Reservations**: Display a list of all current reservations in a tabular format.
* **Update Reservations**: Modify details of existing reservations.
* **Delete Reservations**: Remove reservations from the system.
* User-friendly GUI built with Tkinter.
* Persistent storage using an SQLite database (`flights.db`).
* Multi-page interface for better navigation.

## File Structure


/Simple-Flight-Reservation-Desktop-App-main

├── main.py                 # Main application entry point

├── database.py             # SQLite database connection, setup, and CRUD operations

├── home.py                 # UI for the Home Page

├── booking.py              # UI for the Flight Booking Page

├── reservations.py         # UI for displaying all reservations

├── edit_reservation.py     # UI for editing an existing reservation

├── flights.db              # SQLite database file (created automatically)

├── requirements.txt        # Information about dependencies

├── README.md               # This file

└── .gitignore              # Specifies intentionally untracked files that Git should ignore


## Prerequisites

* Python 3.x (Tkinter and SQLite3 are typically included with standard Python installations)

## Setup and Running the Application

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd flight_reservation_app
    ```
    Alternatively, you can download the source code files (`main.py`, `database.py`, `home.py`, `booking.py`, `reservations.py`, `edit_reservation.py`) and place them in the same directory.

2.  **Navigate to the project directory:**
    Open a terminal or command prompt and change to the directory where you saved/cloned the files.

3.  **Run the application:**
    Execute the `main.py` script:
    ```bash
    python main.py
    ```
    This will launch the application window. The `flights.db` database file will be created automatically in the same directory if it doesn't already exist.

## Using the Application

* **Home Page**:
    * **Book a New Flight**: Navigates to the booking form.
    * **View All Reservations**: Navigates to the list of current reservations.

* **Booking Page**:
    * Fill in all the required fields (Passenger Name, Flight Number, Departure, Destination, Date, Seat Number).
    * Click "Submit Reservation" to save the booking.
    * Click "Back to Home" to return to the main menu.

* **Reservations List Page**:
    * Displays all reservations in a table.
    * **Refresh List**: Reloads the reservations from the database.
    * **Edit Selected**: Select a reservation from the table and click this button to go to the edit page.
    * **Delete Selected**: Select a reservation and click this button to remove it (a confirmation will be asked).
    * **Back to Home**: Returns to the main menu.

* **Edit Reservation Page**:
    * The form will be pre-filled with the selected reservation's details.
    * Modify the necessary fields.
    * Click "Update Reservation" to save changes (a confirmation will be asked).
    * Click "Cancel / Back to List" to return to the reservations list without saving changes.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

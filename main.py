# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import database

from home import HomePage
from booking import BookingPage
from reservations import ReservationsPage
from edit_reservation import EditReservationPage

class FlightReservationApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Simple Flight Reservation System")
        self.geometry("800x600")

        self.db_conn = None
        self.initialize_app_database()

        if not self.db_conn:
            messagebox.showerror("Database Error", "Failed to connect to the database. The application cannot start.")
            self.destroy()
            return

        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            print("Clam theme not available, using default.")
            self.style.theme_use(self.style.theme_names()[0])

        container = ttk.Frame(self, padding="10")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_frame = None

        for F in (HomePage, BookingPage, ReservationsPage, EditReservationPage):
            page_name = F.__name__
            if page_name == "HomePage":
                frame = F(container,
                          show_booking_page_callback=lambda: self.show_frame("BookingPage"),
                          show_reservations_page_callback=lambda: self.show_frame("ReservationsPage"))
            elif page_name == "BookingPage":
                frame = F(container,
                          show_home_page_callback=lambda: self.show_frame("HomePage"),
                          db_connection=self.db_conn)
            elif page_name == "ReservationsPage":
                frame = F(container,
                          show_home_page_callback=lambda: self.show_frame("HomePage"),
                          show_edit_page_callback=self.show_edit_frame_with_id,
                          db_connection=self.db_conn)
            elif page_name == "EditReservationPage":
                frame = F(container,
                          show_reservations_page_callback=lambda: self.show_frame("ReservationsPage"),
                          db_connection=self.db_conn)
            else:
                frame = F(container, self)

            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def initialize_app_database(self):
        try:
            database.initialize_database()
            self.db_conn = database.create_connection()
            if self.db_conn:
                print("Database connection established successfully.")
            else:
                print("Failed to create database connection.")
        except Exception as e:
            print(f"Error during database initialization: {e}")
            self.db_conn = None

    def show_frame(self, page_name_to_show, data_to_pass=None):
        if page_name_to_show not in self.frames:
            print(f"Error: Frame '{page_name_to_show}' not found.")
            return

        frame_to_show = self.frames[page_name_to_show]

        if self.current_frame and self.current_frame != frame_to_show:
            pass 

        frame_to_show.tkraise()
        self.current_frame = frame_to_show
        print(f"Showing frame: {page_name_to_show}")

        if hasattr(frame_to_show, 'on_show'):
            if data_to_pass is not None:
                frame_to_show.on_show(data_to_pass)
            else:
                frame_to_show.on_show()
        
        self.refresh_all_db_connections()

    def show_edit_frame_with_id(self, reservation_id):
        if reservation_id is not None:
            self.show_frame("EditReservationPage", data_to_pass=reservation_id)
        else:
            messagebox.showwarning("Edit Error", "No reservation selected to edit.", parent=self)

    def refresh_all_db_connections(self):
        if not self.db_conn:
            print("Cannot refresh DB connections, main connection is None.")
            return

        for frame_instance in self.frames.values():
            if hasattr(frame_instance, 'refresh_db_connection'):
                try:
                    frame_instance.refresh_db_connection(self.db_conn)
                except Exception as e:
                    print(f"Error refreshing DB connection for {frame_instance.__class__.__name__}: {e}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to exit the application?", parent=self):
            if self.db_conn:
                try:
                    self.db_conn.close()
                    print("Database connection closed successfully.")
                except Exception as e:
                    print(f"Error closing database connection: {e}")
            self.destroy()

if __name__ == "__main__":
    app = FlightReservationApp()
    app.mainloop()
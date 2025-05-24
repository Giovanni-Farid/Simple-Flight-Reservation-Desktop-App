# booking.py
import tkinter as tk
from tkinter import ttk, messagebox
import database

class BookingPage(tk.Frame):
    def __init__(self, master, show_home_page_callback, db_connection):
        super().__init__(master)
        self.master = master
        self.show_home_page = show_home_page_callback
        self.db_conn = db_connection

        self.configure(bg="#f0f0f0")

        title_label = ttk.Label(
            self,
            text="Book a New Flight",
            font=("Arial", 20, "bold"),
            background="#f0f0f0",
            foreground="#333333"
        )
        title_label.pack(pady=(20, 15))

        form_frame = ttk.Frame(self, padding="20 20 20 20", style="TFrame")
        form_frame.pack(expand=True, padx=30, pady=10)

        label_font = ("Arial", 11)
        entry_font = ("Arial", 11)
        entry_width = 40

        fields = [
            ("Passenger Name:", "name_entry"),
            ("Flight Number:", "flight_number_entry"),
            ("Departure City:", "departure_entry"),
            ("Destination City:", "destination_entry"),
            ("Date (YYYY-MM-DD):", "date_entry"),
            ("Seat Number:", "seat_number_entry")
        ]

        self.entries = {}

        for i, (text, entry_name) in enumerate(fields):
            label = ttk.Label(form_frame, text=text, font=label_font, background="#f0f0f0")
            label.grid(row=i, column=0, padx=10, pady=8, sticky="w")

            entry = ttk.Entry(form_frame, font=entry_font, width=entry_width)
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
            self.entries[entry_name] = entry

        form_frame.columnconfigure(1, weight=1)

        buttons_frame = ttk.Frame(self, style="TFrame")
        buttons_frame.pack(pady=(10, 20))

        style = ttk.Style(self)
        style.configure("Booking.TButton",
                        font=("Arial", 12),
                        padding=(10, 5),
                        width=15)
        style.map("Booking.TButton",
                  background=[('active', '#e0e0e0'), ('!active', '#ffffff')],
                  foreground=[('active', '#000000'), ('!active', '#333333')])

        submit_button = ttk.Button(
            buttons_frame,
            text="Submit Reservation",
            command=self.submit_reservation,
            style="Booking.TButton"
        )
        submit_button.pack(side=tk.LEFT, padx=10)

        back_button = ttk.Button(
            buttons_frame,
            text="Back to Home",
            command=self.show_home_page,
            style="Booking.TButton"
        )
        back_button.pack(side=tk.LEFT, padx=10)

        self.status_label = ttk.Label(self, text="", font=("Arial", 10), background="#f0f0f0")
        self.status_label.pack(pady=(0, 10))


    def submit_reservation(self):
        name = self.entries["name_entry"].get().strip()
        flight_number = self.entries["flight_number_entry"].get().strip()
        departure = self.entries["departure_entry"].get().strip()
        destination = self.entries["destination_entry"].get().strip()
        date = self.entries["date_entry"].get().strip()
        seat_number = self.entries["seat_number_entry"].get().strip()

        if not all([name, flight_number, departure, destination, date, seat_number]):
            messagebox.showerror("Error", "All fields are required!", parent=self)
            self.status_label.config(text="Error: All fields are required.", foreground="red")
            return

        reservation_details = (name, flight_number, departure, destination, date, seat_number)

        try:
            reservation_id = database.add_reservation(self.db_conn, reservation_details)
            if reservation_id:
                messagebox.showinfo("Success", f"Reservation successfully booked!\nID: {reservation_id}", parent=self)
                self.status_label.config(text=f"Reservation booked (ID: {reservation_id}).", foreground="green")
                self.clear_form()
            else:
                messagebox.showerror("Database Error", "Failed to book reservation. Check logs.", parent=self)
                self.status_label.config(text="Error: Failed to book reservation.", foreground="red")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}", parent=self)
            self.status_label.config(text=f"Error: {e}", foreground="red")
            print(f"Error during submission: {e}")


    def clear_form(self):
        for entry_widget in self.entries.values():
            entry_widget.delete(0, tk.END)
        self.entries["name_entry"].focus_set()
        self.status_label.config(text="")

    def refresh_db_connection(self, new_conn):
        self.db_conn = new_conn
        print("BookingPage: Database connection refreshed.")

    def on_show(self):
        print("BookingPage is now visible.")
        self.clear_form()
        self.status_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flight Booking Page Test")
    root.geometry("650x500")

    database.initialize_database()
    test_db_conn = database.create_connection()

    if not test_db_conn:
        print("Failed to connect to the database for testing. Exiting.")
        exit()

    style = ttk.Style(root)
    style.theme_use('clam')

    def dummy_show_home():
        print("Dummy: Navigating back to Home Page")
        booking_page_frame.grid_forget()
        tk.Label(root, text="Returned to Home (Test)").pack()


    booking_page_frame = BookingPage(root, dummy_show_home, test_db_conn)
    booking_page_frame.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


    def on_closing():
        if test_db_conn:
            test_db_conn.close()
            print("Test database connection closed.")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

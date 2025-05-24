# edit_reservation.py
import tkinter as tk
from tkinter import ttk, messagebox
import database

class EditReservationPage(tk.Frame):
    def __init__(self, master, show_reservations_page_callback, db_connection):
        super().__init__(master)
        self.master = master
        self.show_reservations_page = show_reservations_page_callback
        self.db_conn = db_connection
        self.current_reservation_id = None

        self.configure(bg="#f0f0f0")

        title_label = ttk.Label(
            self,
            text="Edit Flight Reservation",
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
        style.configure("Edit.TButton",
                        font=("Arial", 12),
                        padding=(10, 5),
                        width=20)
        style.map("Edit.TButton",
                  background=[('active', '#e0e0e0'), ('!active', '#ffffff')],
                  foreground=[('active', '#000000'), ('!active', '#333333')])

        update_button = ttk.Button(
            buttons_frame,
            text="Update Reservation",
            command=self.update_reservation_details,
            style="Edit.TButton"
        )
        update_button.pack(side=tk.LEFT, padx=10)

        cancel_button = ttk.Button(
            buttons_frame,
            text="Cancel / Back to List",
            command=self.go_back_to_reservations,
            style="Edit.TButton"
        )
        cancel_button.pack(side=tk.LEFT, padx=10)

        self.status_label = ttk.Label(self, text="", font=("Arial", 10), background="#f0f0f0")
        self.status_label.pack(pady=(0, 10))

    def load_reservation_details(self, reservation_id):
        self.current_reservation_id = reservation_id
        self.clear_form(clear_status=False)
        
        if self.current_reservation_id is None:
            messagebox.showerror("Error", "No reservation ID provided to edit.", parent=self)
            self.status_label.config(text="Error: No reservation ID.", foreground="red")
            self.show_reservations_page()
            return

        try:
            reservation_data = database.get_reservation_by_id(self.db_conn, self.current_reservation_id)
            if reservation_data:
                self.entries["name_entry"].insert(0, reservation_data[1])
                self.entries["flight_number_entry"].insert(0, reservation_data[2])
                self.entries["departure_entry"].insert(0, reservation_data[3])
                self.entries["destination_entry"].insert(0, reservation_data[4])
                self.entries["date_entry"].insert(0, reservation_data[5])
                self.entries["seat_number_entry"].insert(0, reservation_data[6])
                self.status_label.config(text=f"Editing Reservation ID: {self.current_reservation_id}", foreground="blue")
            else:
                messagebox.showerror("Error", f"Reservation ID: {self.current_reservation_id} not found.", parent=self)
                self.status_label.config(text=f"Error: Reservation ID {self.current_reservation_id} not found.", foreground="red")
                self.show_reservations_page()
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load reservation details: {e}", parent=self)
            self.status_label.config(text=f"Error loading details: {e}", foreground="red")
            print(f"Error loading reservation details: {e}")
            self.show_reservations_page()

    def update_reservation_details(self):
        if self.current_reservation_id is None:
            messagebox.showerror("Error", "No reservation selected for update.", parent=self)
            self.status_label.config(text="Error: No reservation to update.", foreground="red")
            return

        name = self.entries["name_entry"].get().strip()
        flight_number = self.entries["flight_number_entry"].get().strip()
        departure = self.entries["departure_entry"].get().strip()
        destination = self.entries["destination_entry"].get().strip()
        date = self.entries["date_entry"].get().strip()
        seat_number = self.entries["seat_number_entry"].get().strip()

        if not all([name, flight_number, departure, destination, date, seat_number]):
            messagebox.showerror("Error", "All fields are required!", parent=self)
            self.status_label.config(text="Error: All fields must be filled.", foreground="red")
            return

        updated_details = (name, flight_number, departure, destination, date, seat_number)

        try:
            confirm = messagebox.askyesno("Confirm Update",
                                           f"Are you sure you want to update reservation ID: {self.current_reservation_id}?",
                                           parent=self)
            if confirm:
                success = database.update_reservation(self.db_conn, self.current_reservation_id, updated_details)
                if success:
                    messagebox.showinfo("Success", f"Reservation ID: {self.current_reservation_id} updated successfully.", parent=self)
                    self.status_label.config(text="Reservation updated successfully!", foreground="green")
                    self.show_reservations_page()
                else:
                    messagebox.showerror("Update Error", f"Failed to update reservation ID: {self.current_reservation_id}.", parent=self)
                    self.status_label.config(text="Error: Failed to update reservation.", foreground="red")
        except Exception as e:
            messagebox.showerror("Update Error", f"An unexpected error occurred: {e}", parent=self)
            self.status_label.config(text=f"Error: {e}", foreground="red")
            print(f"Error during update: {e}")

    def clear_form(self, clear_status=True):
        for entry_widget in self.entries.values():
            entry_widget.delete(0, tk.END)
        if clear_status:
            self.status_label.config(text="")

    def go_back_to_reservations(self):
        self.clear_form()
        self.current_reservation_id = None
        self.show_reservations_page()

    def refresh_db_connection(self, new_conn):
        self.db_conn = new_conn
        print("EditReservationPage: Database connection refreshed.")

    def on_show(self, reservation_id):
        print(f"EditReservationPage is now visible for ID: {reservation_id}. Loading details.")
        self.load_reservation_details(reservation_id)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Edit Reservation Page Test")
    root.geometry("650x550")

    database.initialize_database()
    test_db_conn = database.create_connection()

    if not test_db_conn:
        print("Failed to connect to the database for testing. Exiting.")
        exit()

    TEST_RES_ID = None
    try:
        TEST_RES_ID = database.add_reservation(test_db_conn, ("Edit Test User", "ET001", "Testville", "Debug City", "2025-01-15", "X1"))
        if TEST_RES_ID:
            print(f"Added test reservation with ID: {TEST_RES_ID} for editing.")
        else:
            print("Failed to add test reservation for editing.")
            test_db_conn.close()
            exit()
    except Exception as e:
        print(f"Error setting up test data: {e}")
        test_db_conn.close()
        exit()

    style = ttk.Style(root)
    style.theme_use('clam')

    def dummy_show_reservations_list():
        print("Dummy: Navigating back to Reservations List Page")
        edit_page_frame.pack_forget()
        tk.Label(root, text="Returned to Reservations List (Test)").pack()

    edit_page_frame = EditReservationPage(root, dummy_show_reservations_list, test_db_conn)
    edit_page_frame.pack(fill=tk.BOTH, expand=True)

    if TEST_RES_ID:
        edit_page_frame.load_reservation_details(TEST_RES_ID)
    else:
        tk.Label(root, text="Error: Could not load test reservation ID for editing.").pack()

    def on_closing():
        if test_db_conn:
            if TEST_RES_ID:
                database.delete_reservation(test_db_conn, TEST_RES_ID)
                print(f"Deleted test reservation ID: {TEST_RES_ID}")
            test_db_conn.close()
            print("Test database connection closed.")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
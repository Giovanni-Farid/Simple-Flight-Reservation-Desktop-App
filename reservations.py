# reservations.py
import tkinter as tk
from tkinter import ttk, messagebox
import database

class ReservationsPage(tk.Frame):
    def __init__(self, master, show_home_page_callback, show_edit_page_callback, db_connection):
        super().__init__(master)
        self.master = master
        self.show_home_page = show_home_page_callback
        self.show_edit_page = show_edit_page_callback
        self.db_conn = db_connection

        self.configure(bg="#f0f0f0")

        title_label = ttk.Label(
            self,
            text="Current Flight Reservations",
            font=("Arial", 20, "bold"),
            background="#f0f0f0",
            foreground="#333333"
        )
        title_label.pack(pady=(20, 10))

        tree_frame = ttk.Frame(self, padding="10")
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=5)

        columns = ("id", "name", "flight_number", "departure", "destination", "date", "seat_number")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Passenger Name")
        self.tree.heading("flight_number", text="Flight No.")
        self.tree.heading("departure", text="Departure")
        self.tree.heading("destination", text="Destination")
        self.tree.heading("date", text="Date")
        self.tree.heading("seat_number", text="Seat No.")

        self.tree.column("id", width=40, minwidth=30, stretch=tk.NO, anchor=tk.CENTER)
        self.tree.column("name", width=150, minwidth=100)
        self.tree.column("flight_number", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("departure", width=120, minwidth=100)
        self.tree.column("destination", width=120, minwidth=100)
        self.tree.column("date", width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column("seat_number", width=80, minwidth=60, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.pack(expand=True, fill=tk.BOTH)

        buttons_frame = ttk.Frame(self, style="TFrame", padding="10")
        buttons_frame.pack(pady=(5, 15))

        style = ttk.Style(self) 
        style.configure("Reservations.TButton",
                        font=("Arial", 12),
                        padding=(10, 5),
                        width=15) 
        style.map("Reservations.TButton",
                  background=[('active', '#e0e0e0'), ('!active', '#ffffff')],
                  foreground=[('active', '#000000'), ('!active', '#333333')])

        refresh_button = ttk.Button(
            buttons_frame,
            text="Refresh List",
            command=self.load_reservations,
            style="Reservations.TButton"
        )
        refresh_button.pack(side=tk.LEFT, padx=5)

        edit_button = ttk.Button(
            buttons_frame,
            text="Edit Selected",
            command=self.edit_selected_reservation,
            style="Reservations.TButton"
        )
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_selected_reservation,
            style="Reservations.TButton"
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        back_button = ttk.Button(
            buttons_frame,
            text="Back to Home",
            command=self.show_home_page,
            style="Reservations.TButton"
        )
        back_button.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(self, text="", font=("Arial", 10), background="#f0f0f0")
        self.status_label.pack(pady=(0,10))

    def load_reservations(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            if not self.db_conn or getattr(self.db_conn, 'closed', False): 
                messagebox.showerror("Database Error", "Database connection is not available.", parent=self)
                self.status_label.config(text="Error: Database connection lost.", foreground="red")
                return

            reservations_data = database.get_all_reservations(self.db_conn)
            if reservations_data:
                for row in reservations_data:
                    self.tree.insert("", tk.END, values=row)
                self.status_label.config(text=f"Loaded {len(reservations_data)} reservations.", foreground="green")
            else:
                self.status_label.config(text="No reservations found.", foreground="black")
        except Exception as e: 
            messagebox.showerror("Load Error", f"Failed to load reservations: {e}", parent=self)
            self.status_label.config(text=f"Error loading reservations: {e}", foreground="red")
            print(f"Error loading reservations: {e}")

    def get_selected_reservation_id(self):
        selected_item = self.tree.focus() 
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a reservation from the list first.", parent=self)
            return None
        
        item_details = self.tree.item(selected_item)
        try:
            reservation_id = item_details['values'][0] 
            return reservation_id
        except (IndexError, TypeError):
            messagebox.showerror("Error", "Could not retrieve reservation ID from selection.", parent=self)
            return None

    def edit_selected_reservation(self):
        reservation_id = self.get_selected_reservation_id()
        if reservation_id is not None:
            print(f"Attempting to edit reservation ID: {reservation_id}")
            self.show_edit_page(reservation_id)

    def delete_selected_reservation(self):
        reservation_id = self.get_selected_reservation_id()
        if reservation_id is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete reservation ID: {reservation_id}?",
            parent=self
        )

        if confirm:
            try:
                if not self.db_conn or getattr(self.db_conn, 'closed', False):
                     messagebox.showerror("Database Error", "Database connection is not available.", parent=self)
                     return

                success = database.delete_reservation(self.db_conn, reservation_id)
                if success:
                    messagebox.showinfo("Success", f"Reservation ID: {reservation_id} deleted successfully.", parent=self)
                    self.status_label.config(text=f"Reservation ID: {reservation_id} deleted.", foreground="green")
                    self.load_reservations() 
                else:
                    messagebox.showerror("Delete Error", f"Failed to delete reservation ID: {reservation_id}.", parent=self)
                    self.status_label.config(text=f"Error deleting reservation ID: {reservation_id}.", foreground="red")
            except Exception as e:
                messagebox.showerror("Delete Error", f"An error occurred: {e}", parent=self)
                self.status_label.config(text=f"Error: {e}", foreground="red")
                print(f"Error deleting reservation: {e}")

    def refresh_db_connection(self, new_conn):
        self.db_conn = new_conn
        print("ReservationsPage: Database connection refreshed.")

    def on_show(self):
        print("ReservationsPage is now visible. Refreshing list.")
        self.load_reservations()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reservations List Page Test")
    root.geometry("900x600") 

    database.initialize_database()
    test_db_conn = database.create_connection()

    if not test_db_conn:
        print("Failed to connect to the database for testing. Exiting.")
        exit()
    
    style = ttk.Style(root)
    style.theme_use('clam')

    def dummy_show_home():
        print("Dummy: Navigating back to Home Page")
        reservations_page_frame.grid_forget()
        tk.Label(root, text="Returned to Home (Test)").grid(row=0, column=0, sticky="nsew")

    def dummy_show_edit(res_id):
        print(f"Dummy: Navigating to Edit Page for Reservation ID: {res_id}")
        edit_window = tk.Toplevel(root) 
        edit_window.title(f"Edit Reservation {res_id} (Test)")
        edit_window.geometry("400x300")
        tk.Label(edit_window, text=f"This is the edit page for reservation ID: {res_id}.").pack(padx=20, pady=20)

    reservations_page_frame = ReservationsPage(root, dummy_show_home, dummy_show_edit, test_db_conn)
    reservations_page_frame.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    reservations_page_frame.on_show() 

    def on_closing():
        if test_db_conn:
            test_db_conn.close()
            print("Test database connection closed.")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

# home.py
import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, master, show_booking_page_callback, show_reservations_page_callback):
        super().__init__(master)
        self.master = master
        self.show_booking_page = show_booking_page_callback
        self.show_reservations_page = show_reservations_page_callback

        self.configure(bg="#f0f0f0")

        title_label = ttk.Label(
            self,
            text="Flight Reservation System",
            font=("Arial", 24, "bold"),
            background="#f0f0f0",
            foreground="#333333"
        )
        title_label.pack(pady=(30, 20))

        options_frame = ttk.Frame(self, style="TFrame")
        options_frame.pack(pady=20, padx=20, fill=tk.X)

        style = ttk.Style(self)
        style.configure("Home.TButton",
                        font=("Arial", 14),
                        padding=(20, 10),
                        width=25,
                        borderwidth=1,
                        relief="flat",
                       )
        style.map("Home.TButton",
                  background=[('active', '#e0e0e0'), ('!active', '#ffffff')],
                  foreground=[('active', '#000000'), ('!active', '#333333')]
                 )

        book_button = ttk.Button(
            options_frame,
            text="Book a New Flight",
            command=self.show_booking_page,
            style="Home.TButton"
        )
        book_button.pack(pady=15, fill=tk.X, padx=50)

        view_button = ttk.Button(
            options_frame,
            text="View All Reservations",
            command=self.show_reservations_page,
            style="Home.TButton"
        )
        view_button.pack(pady=15, fill=tk.X, padx=50)

        self.status_bar = ttk.Label(
            self,
            text="Welcome! Please select an option.",
            font=("Arial", 10),
            background="#f0f0f0",
            foreground="#555555",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, ipady=5)

    def on_show(self):
        print("HomePage is now visible.")
        self.status_bar.config(text="Welcome! Please select an option.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Home Page Test")
    root.geometry("500x400")

    if not hasattr(root, 'style'):
         root.style = ttk.Style(root)
         root.style.theme_use('clam')

    def dummy_show_booking():
        print("Dummy: Show Booking Page")
        home_page_frame.grid_forget()
        tk.Label(root, text="Navigated to Booking Page (Test)").grid(row=0, column=0, sticky="nsew")

    def dummy_show_reservations():
        print("Dummy: Show Reservations Page")
        home_page_frame.grid_forget()
        tk.Label(root, text="Navigated to Reservations Page (Test)").grid(row=0, column=0, sticky="nsew")

    home_page_frame = HomePage(root, dummy_show_booking, dummy_show_reservations)
    home_page_frame.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()
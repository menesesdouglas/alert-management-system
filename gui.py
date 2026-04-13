from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import queries as qrs
from tkcalendar import DateEntry
from datetime import datetime
from time import sleep as sp
import threading

class Application(Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.grid()
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.create_widgets()

        self.thread_verify = threading.Thread(target=self.verify_pending_allerts, daemon=True)
        self.thread_verify.start()

    def create_widgets(self):
        self.allert = tk.StringVar()
        self.allert.set("")
        self.allert_index = tk.IntVar()

        self.main_frame = Frame(self, padx=10, pady=10, bg="#f0f0f0")
        self.main_frame.grid()

        Label(self.main_frame, text="Alert Text:", bg="#f0f0f0", font=('Arial', 10)).grid(row=0, column=0, sticky=W, pady=5)
        self.entry1 = Entry(self.main_frame, width=30, textvariable=self.allert, font=('Arial', 10), bd=2, relief=GROOVE)
        self.entry1.grid(row=0, column=1, pady=5)

        Label(self.main_frame, text="Select the date of the alert:", bg="#f0f0f0", font=('Arial', 10)).grid(row=1, column=0, sticky=W, pady=5)
        self.date_selected = DateEntry(
            self.main_frame,
            width=12,
            background="white",
            foreground="black",
            borderwidth=2,
            year=datetime.now().year,
            date_pattern='dd/mm/yyyy',
            font=('Arial', 10)
        )
        self.date_selected.grid(row=1, column=1, pady=5)

        Label(self.main_frame, text="Select the time of the alert:", bg="#f0f0f0", font=('Arial', 10)).grid(row=2, column=0, sticky=W, pady=5)
        self.time_frame = Frame(self.main_frame, bg="#f0f0f0")
        self.time_frame.grid(row=2, column=1, pady=5)

        self.hour_spinbox = Spinbox(self.time_frame, from_=0, to=23, width=3, wrap=True, font=('Arial', 10))
        self.hour_spinbox.pack(side=LEFT)
        Label(self.time_frame, text=":", bg="#f0f0f0", font=('Arial', 10)).pack(side=LEFT)
        self.minute_spinbox = Spinbox(self.time_frame, from_=0, to=59, width=3, wrap=True, font=('Arial', 10))
        self.minute_spinbox.pack(side=LEFT)

        self.bttn1 = Button(self.main_frame, text="Create Alert", command=self.insert_allert_from_entry_to_db, font=('Arial', 10), bg="#4CAF50", fg="white")
        self.bttn1.grid(row=3, column=0, columnspan=2, pady=10, sticky=EW)

        Label(self.main_frame, text="Alert ID:", bg="#f0f0f0", font=('Arial', 10)).grid(row=4, column=0, sticky=W, pady=5)
        self.entry2 = Entry(self.main_frame, width=10, textvariable=self.allert_index, font=('Arial', 10), bd=2, relief=GROOVE)
        self.entry2.grid(row=4, column=1, sticky=W, pady=5)

        self.bttn2 = Button(self.main_frame, text="Get Alert", command=self.get_allert_from_entry, font=('Arial', 10), bg="#2196F3", fg="white")
        self.bttn2.grid(row=5, column=0, pady=5, sticky=EW)

        self.bttn3 = Button(self.main_frame, text="Get All Alerts", command=self.get_all_allerts, font=('Arial', 10), bg="#2196F3", fg="white")
        self.bttn3.grid(row=5, column=1, pady=5, sticky=EW)

        self.bttn4 = Button(self.main_frame, text="Get Canceled Alerts", command=self.get_all_canceled_allerts, font=('Arial', 10), bg="#FF9800", fg="white")
        self.bttn4.grid(row=6, column=0, pady=5, sticky=EW)

        self.bttn5 = Button(self.main_frame, text="Cancel Alert", command=self.cancel_allert, font=('Arial', 10), bg="#F44336", fg="white")
        self.bttn5.grid(row=6, column=1, pady=5, sticky=EW)

    def insert_allert_from_entry_to_db(self):
        try:
            allert_text = self.allert.get()
            selected_date = self.date_selected.get_date()
            selected_hour = int(self.hour_spinbox.get())
            selected_minute = int(self.minute_spinbox.get())

            full_datetime = datetime(
                year=selected_date.year,
                month=selected_date.month,
                day=selected_date.day,
                hour=selected_hour,
                minute=selected_minute
            )

            qrs.insert_allert_to_db(allert_text, full_datetime)
            success_message = "Alert inserted successfully!"
            self.popups(success_message)

        except Exception as e:
            message_error = f"An error occurred while inserting the alert: {e}"
            self.popups(message_error)

    def get_allert_from_entry(self):
        try:
            allert_id = self.allert_index.get()
            allert = qrs.select_allerts_from_db_by_id(allert_id)
            formatted_allert = self.format_dataframe_to_string(allert)
            self.popups(formatted_allert)
        except Exception as e:
            message_error = f"An error occurred while fetching the alert: {e}"
            self.popups(message_error)

    def get_all_allerts(self):
        try:
            allerts = qrs.select_allerts_from_db()
            formatted_allerts = self.format_dataframe_to_string(allerts)
            self.popups(formatted_allerts)
        except Exception as e:
            message_error = f'An error occurred while fetching all alerts: {e}'
            self.popups(message_error)

    def get_all_canceled_allerts(self):
        try:
            allerts = qrs.select_canceled_allerts_from_db()
            formatted_allerts = self.format_dataframe_to_string(allerts)
            self.popups(formatted_allerts)
        except Exception as e:
            message_error = f'An error occurred while fetching all alerts: {e}'
            self.popups(message_error)

    def cancel_allert(self):
        try:
            allert_index = self.allert_index.get()
            formatted_allert = self.format_dataframe_to_string(qrs.select_allerts_from_db_by_id(allert_index))
            if formatted_allert == "No alerts found.":
                self.popups(f"No alert found with ID {allert_index}.")
                return
            qrs.update_allert_status_in_db(allert_index, 3)
            self.after(0, lambda: self.popups(f"Alert with ID {allert_index} canceled successfully!"))
        except Exception as e:
            self.after(0, lambda: self.popups(f"An error occurred while canceling the alert with ID {allert_index}: {e}"))
    
    def format_dataframe_to_string(self, df):
        if df.empty:
            return "No alerts found."
        
        result = []
        for _, row in df.iterrows():
            row_str = "\n".join([f"{col}: {val}" for col, val in row.items()])
            result.append(row_str)
            return "\n\n".join(result)

    def verify_pending_allerts(self):
        while True:
            try:
                pending_allerts = qrs.select_pending_allerts_from_db()
                now = datetime.now()

                for _, allert in pending_allerts.iterrows():
                    try:
                        allert_datetime = allert['Data_Aviso']

                        if now >= allert_datetime:
                            self.after(0, lambda msg=allert['Aviso']: self.popups(msg))
                            qrs.update_allert_status_in_db(allert['Código'], 2)

                    except Exception as e:
                        print(f"Error processing alert: {e}")

            except Exception as e:
                print(f"Error verifying pending alerts: {e}")

            sp(5)

    def popups(self, advise):
        messagebox.showinfo(
            title="Alert",
            message=f"{advise}"
        )
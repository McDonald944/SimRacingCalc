import tkinter as tk
import csv
import os
from tkinter import ttk, filedialog, messagebox
import openpyxl
from datetime import datetime


def check_roster_data(filepath):
    """Reads event data (first two lines) and returns race length."""
    try:
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File not found at path: {filepath}")
            return None

        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            event_data = next(reader)

            if len(header) != 5 or len(event_data) != 5:
                messagebox.showerror("Error", "Incorrect number of columns in event data.")
                return None

            next(reader, None)

            try:
                race_length_str = event_data[4]
                try:
                    race_length = int(race_length_str)
                except ValueError:
                    try:
                        hours, minutes = map(int, race_length_str.split(":"))  # Corrected conversion
                        race_length = hours * 60 + minutes
                    except (ValueError, IndexError) as e:
                        messagebox.showerror("Error",
                                             f"Invalid 'Race Length' format (must be number or HH:MM). Error: {e}")
                        return None
            except IndexError:
                messagebox.showerror("Error", "Race Length not found in event data.")
                return None

            return race_length

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return None
    except StopIteration:  # Catch if there are not enough lines in the file
        messagebox.showerror("Error", "Not enough lines in the file.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return None

def generate_availability_sheet(roster_df, start_gmt, start_local, offset, time_block):
    """
    This function generates an Excel availability sheet based on the provided data.

    Args:
        roster_df (pandas.DataFrame): DataFrame containing roster data.
        start_gmt (str): Race start time in GMT format (e.g., "2023-12-31 14:00:00").
        start_local (str): Race start time in local time format (e.g., "2023-12-31 08:00:00").
        offset (str): Green flag offset in minutes (e.g., "30").
        time_block (int): Time block duration in minutes (e.g., 15, 30).
    """
    try:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Driver Availability"

        # Header row
        sheet.append(["Driver Name", "Timezone", "Available"])

        # Process each driver
        for index, row in roster_df.iterrows():
            driver_name = row["Driver Name"]
            timezone = row["Timezone"]
            available_times = []

            # Convert start times to datetime objects
            start_gmt_dt = datetime.strptime(start_gmt, "%Y-%m-%d %H:%M:%S")
            start_local_dt = datetime.strptime(start_local, "%Y-%m-%d %H:%M:%S")

            # Calculate race start time with offset in the driver's timezone
            offset_dt = datetime.strptime(offset, "%M")
            race_start_driver_tz = start_local_dt + datetime.timedelta(minutes=int(offset)) - start_gmt_dt

            # Iterate through time blocks and check availability (modify as needed)
            current_time = race_start_driver_tz
            while current_time < race_start_driver_tz + datetime.timedelta(hours=3):
                available_times.append(current_time.strftime("%H:%M"))
                current_time += datetime.timedelta(minutes=time_block)

            sheet.append([driver_name, timezone, ",".join(available_times)])

        wb.save("Driver_Availability.xlsx")
        messagebox.showinfo("Success", "Driver Availability sheet generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating Excel sheet: {str(e)}")

def open_availability_window(master):
    """
    This function opens a new window for driver availability input.

    Args:
        master (tk.Tk): The main application window.
    """

    def open_availability_window(master):
        """
        This function opens a new window for driver availability input.

        Args:
            master (tk.Tk): The main application window.
        """

    def open_roster_file():
        """Opens a file dialog to select the roster CSV file."""
        filepath = filedialog.askopenfilename(defaultextension=".csv",
                                              filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                              title="Select Roster File")
        if filepath:
            roster_df = check_roster_data(filepath)
            if roster_df is not None:
                create_availability_input_window(master, roster_df)

    def create_availability_input_window(master, roster_df):
        # Create the window
        availability_window = tk.Toplevel(master)
        availability_window.title("Driver Availability Input")
        availability_window.geometry("400x300")  # Adjust window size
        availability_window.resizable(False, False)


        # Input fields
        ttk.Label(availability_window, text="Race Start Time (GMT):", font=("Arial", 12)).grid(row=0, column=0,
                                                                                               sticky="w", padx=10,
                                                                                               pady=5)
        start_gmt_entry = ttk.Entry(availability_window, width=20)
        start_gmt_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(availability_window, text="Race Start Time (Local):", font=("Arial", 12)).grid(row=1, column=0,
                                                                                                 sticky="w", padx=10,
                                                                                                 pady=5)
        start_local_entry = ttk.Entry(availability_window, width=20)
        start_local_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(availability_window, text="Green Flag Offset (minutes):", font=("Arial", 12)).grid(row=2, column=0,
                                                                                                     sticky="w",
                                                                                                     padx=10, pady=5)
        offset_entry = ttk.Entry(availability_window, width=20)
        offset_entry.insert(0, "30")
        offset_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        # Time Block Frame (Vertical Layout)
        time_block_frame = ttk.Frame(availability_window)
        time_block_frame.grid(row=3, column=1, sticky="nsew", padx=10, pady=5)  # Place the frame
        availability_window.rowconfigure(3, weight=1)

        time_block_label = ttk.Label(availability_window, text="Time Block:", font=("Arial", 12))
        time_block_label.grid(row=3, column=0, sticky="nw", padx=10, pady=5)
        time_block = tk.IntVar(value=15)

        time_block_values = [15, 30, 45, 60]
        for i, value in enumerate(time_block_values):
            ttk.Radiobutton(time_block_frame, text=f"{value} Minutes", variable=time_block, value=value).grid(row=i,
                                                                                                              column=0,
                                                                                                              sticky="w",
                                                                                                              pady=2)

        # Center the window (using update_idletasks)
        availability_window.update_idletasks()
        width = availability_window.winfo_width()
        height = availability_window.winfo_height()
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        availability_window.geometry("+{}+{}".format(x, y))

        def create_availability():
            start_gmt = start_gmt_entry.get()
            start_local = start_local_entry.get()
            offset = offset_entry.get()
            if not start_gmt or not start_local:
                messagebox.showerror("Error", "Race Start Times (GMT and Local) are required.")
                return
            generate_availability_sheet(race_length, start_gmt, start_local, offset, time_block.get())

        create_button = ttk.Button(availability_window, text="Create Availability Sheet", command=create_availability)
        create_button.grid(row=4, column=0, columnspan=2, pady=10)

    open_roster_file()
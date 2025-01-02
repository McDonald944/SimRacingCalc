import csv
import os
from tkinter import messagebox, filedialog
import pandas as pd

def save_roster_data(event_data, roster_data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write event data as a header row
            writer.writerow(["Event Name", "Team Name", "Track", "Car", "Race Length"])
            writer.writerow(event_data)
            writer.writerow([]) #Blank row for spacing
            # Write driver data
            writer.writerow(["iRating", "Driver Name", "Back to Back Stints", "Triple Stint", "Timezone", "Start", "Finish"])
            writer.writerows(roster_data)
        return True  # Indicate success
    except Exception as e:
        print(f"Error saving data: {e}")
        return False #Indicate failure

def load_roster_data(filename):
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            event_header = next(reader)  # Read and discard event header
            event_data = next(reader)      # Read the actual event data
            next(reader) #Skip blank row
            driver_header = next(reader) #Read and discard driver header
            roster_data = list(reader)  # Read the rest as driver data
        return event_data, roster_data
    except StopIteration: #Handle empty files
        return [], []
    except FileNotFoundError:
        raise
    except Exception as e:
        print(f"Error loading data: {e}")
        raise #Re-raise the exception

def open_roster_file():
    """Opens a file dialog and returns the selected file path or None if cancelled."""
    filepath = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], title="Select Roster File")
    if filepath:  # Check if a file was actually selected
        return filepath
    else:
        return None  # Return None if the dialog was cancelled

def check_roster_data(filepath):
    if filepath is None:
        return None
    try:
        data = []
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    data.append(row)

        if len(data) < 4:
            messagebox.showerror("Error", "Roster file must contain event and driver data.")
            return None

        # Correctly create event_data dictionary
        event_data = {}
        for i in range(len(data[0])):  # Iterate through the columns
            if i < len(data[1]): #check to make sure the index exists in the second row
                event_data[data[0][i]] = data[1][i]
            else:
                event_data[data[0][i]] = "" #if it doesnt exist, make it an empty string

        if "Race Length" not in event_data:
            messagebox.showerror("Error", "Roster file must contain 'Race Length' data.")
            return None

        driver_data = data[3:]
        if not driver_data or not driver_data[0]:
            messagebox.showerror("Error", "Roster file must contain driver data.")
            return None
        driver_df = pd.DataFrame(driver_data[1:], columns=driver_data[0])

        return event_data["Race Length"], driver_df

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return None
    except IndexError as e:
        messagebox.showerror("Error", f"Invalid roster file format (Index Error): {e}")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return None
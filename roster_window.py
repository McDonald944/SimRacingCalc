import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import data_handling as dh
import pytz

timezone_mapping = {
    # North America
    "EST": "America/New_York",
    "CST": "America/Chicago",
    "MST": "America/Denver",
    "PST": "America/Los_Angeles",
    "AKST": "America/Anchorage",  # Alaska Standard Time
    "HST": "Pacific/Honolulu",    # Hawaii Standard Time
    "EDT": "America/New_York",  #Eastern Daylight Time
    "CDT": "America/Chicago",  #Central Daylight Time
    "MDT": "America/Denver",  #Mountain Daylight Time
    "PDT": "America/Los_Angeles",  #Pacific Daylight Time
    "ADT": "America/Halifax", #Atlantic Daylight Time
    "NST": "America/St_Johns", #Newfoundland Standard Time
    "AST": "America/Puerto_Rico", #Atlantic Standard Time

    # Europe
    "GMT": "UTC",  # Use UTC for GMT
    "BST": "Europe/London",
    "CET": "Europe/Berlin",
    "CEST": "Europe/Berlin",
    "EET": "Europe/Athens",
    "EEST": "Europe/Athens",
    "WET": "Europe/Lisbon",
    "WEST": "Europe/Lisbon",

    # Australia
    "AEST": "Australia/Sydney",
    "AEDT": "Australia/Sydney",
    "ACST": "Australia/Adelaide",
    "ACDT": "Australia/Adelaide",
    "AWST": "Australia/Perth",

    # Asia
    "JST": "Asia/Tokyo",
    "IST": "Asia/Kolkata",  # India Standard Time
    "ChST": "Asia/Shanghai", #China Standard Time
    "KST": "Asia/Seoul", #Korea Standard Time

    # Other
    "MSK": "Europe/Moscow",
    "UTC": "UTC",
    "Z": "UTC", #Zulu Time
}

def open_team_roster(master):
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def add_driver():
        nonlocal driver_row_counter
        try:
            if not driver_entries:
                driver_entries.append([])
                driver_row_counter = 1
                create_entry_row()

            new_driver_data = []
            current_row_entries = driver_entries[driver_row_counter - 1]

            back_to_back = False
            triple_stint = False
            start_check = False
            finish_check = False

            for i, col_name in enumerate(column_names):
                try:
                    entry = current_row_entries[i]
                except IndexError:
                    raise ValueError(f"Error accessing entry at index {i}")

                if col_name == "Back to Back Stints":
                    if hasattr(entry, 'var'):
                        back_to_back = entry.var.get()
                        new_driver_data.append(back_to_back)
                    else:
                        new_driver_data.append(False)
                elif col_name == "Triple Stint":
                    if hasattr(entry, 'var'):
                        triple_stint = entry.var.get()
                        new_driver_data.append(triple_stint)
                    else:
                        new_driver_data.append(False)
                elif col_name == "Start":  # handle start check box
                    if hasattr(entry, 'var'):
                        start_check = entry.var.get()
                        new_driver_data.append(start_check)
                    else:
                        new_driver_data.append(False)
                elif col_name == "Finish":  # handle finish check box
                    if hasattr(entry, 'var'):
                        finish_check = entry.var.get()
                        new_driver_data.append(finish_check)
                    else:
                        new_driver_data.append(False)
                elif col_name == "Timezone":
                    if hasattr(entry, 'get'):
                        timezone_str = entry.get()
                        if timezone_str in timezone_mapping:
                            new_driver_data.append(timezone_mapping[timezone_str])
                        else:
                            messagebox.showerror("Unknown Timezone", f"Unknown timezone: {timezone_str}")
                            return
                    else:
                        new_driver_data.append("UTC")
                else:
                    if hasattr(entry, 'get'):
                        try:
                            value = entry.get()
                            if col_name == "iRating":
                                int(value)
                            new_driver_data.append(value)
                        except ValueError:
                            raise ValueError(f"{col_name} must be a number or valid input")
                    else:
                        new_driver_data.append("")

            if triple_stint and not back_to_back:
                raise ValueError("Drivers cannot agree to a Triple Stint without agreeing to Back to Back Stints.")

            tree.insert("", tk.END, values=new_driver_data)

            # Clear input fields (Corrected and Simplified)
            for entry in driver_entries[driver_row_counter - 1]:
                if isinstance(entry, ttk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.current(0)  # set the combobox back to the first value
                elif isinstance(entry, ttk.Checkbutton):
                    entry.var.set(False)

            # Row creation and destruction (Corrected)
            if driver_row_counter == len(driver_entries):
                driver_entries.append([])
                driver_row_counter += 1
                create_entry_row()
            else:
                old_row = driver_entries[driver_row_counter - 1]
                driver_entries[driver_row_counter - 1] = []
                for widget in old_row:
                    widget.grid_forget()
                    widget.destroy()
                for col_num, col_name in enumerate(column_names):
                    if col_name in ["Back to Back Stints", "Triple Stint", "Start", "Finish"]:
                        var = tk.BooleanVar(value=False)
                        entry = ttk.Checkbutton(entry_frame, variable=var)
                        entry.var = var
                    elif col_name == "Timezone":
                        var = tk.StringVar(value=list(timezone_mapping.keys())[
                            0])  # set the default value to the first key in the dict
                        entry = ttk.Combobox(entry_frame, textvariable=var, values=list(timezone_mapping.keys()))
                        entry.var = var
                    else:
                        entry = ttk.Entry(entry_frame)
                    driver_entries[driver_row_counter - 1].append(entry)
                    entry.grid(row=driver_row_counter - 1, column=col_num, padx=5, pady=2, sticky="ew")

            if driver_row_counter > 1:
                old_row_index = driver_row_counter - 2
                for widget in driver_entries[old_row_index]:
                    widget.grid_forget()
                    widget.destroy()
                driver_entries.pop(old_row_index)
                driver_row_counter -= 1

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

    def create_entry_row():
        nonlocal driver_row_counter
        for col_num, col_name in enumerate(column_names):
            var = None
            entry = None
            if col_name in ["Back to Back Stints", "Triple Stint", "Start", "Finish"]:
                var = tk.BooleanVar(value=False)
                entry = ttk.Checkbutton(entry_frame, variable=var)
                entry.var = var
            elif col_name == "Timezone":
                var = tk.StringVar(value=list(timezone_mapping.keys())[0]) #set the default value to the first key in the dict
                entry = ttk.Combobox(entry_frame, textvariable=var, values=list(timezone_mapping.keys()))
                entry.var = var
            else:
                entry = ttk.Entry(entry_frame)
            driver_entries[driver_row_counter - 1].append(entry)
            if entry:
                entry.grid(row=0, column=col_num, padx=5, pady=2, sticky="ew")

    def save_roster():
        event_data = [entry.get() for entry in event_entries]
        roster_data = []
        for item in tree.get_children():
            roster_data.append(tree.item(item)['values'])

        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                                title="Save Roster")
        if filename:  # Check if a filename was selected
            if dh.save_roster_data(event_data, roster_data, filename):
                messagebox.showinfo("Roster Saved", f"Roster saved to {filename}")
                roster_window.destroy()
            else:
                messagebox.showerror("Error Saving Roster", "An error occurred while saving the roster.")
        else:
            messagebox.showinfo("Save Cancelled", "Save was cancelled")
    def delete_driver(event):
        try:
            item = tree.identify_row(event.y)
            if item:
                index = tree.index(item)
                tree.delete(item)

                if driver_entries and index < len(driver_entries):
                    for widget in driver_entries[index]:
                        if isinstance(widget, (ttk.Entry, ttk.Combobox, ttk.Checkbutton)):
                            widget.grid_forget()
                            widget.destroy()
                    driver_entries.pop(index)

                    nonlocal driver_row_counter
                    if driver_row_counter > 1:
                        driver_row_counter -= 1
                        driver_entries.pop() #Call regrid function

                if not driver_entries:
                    driver_entries.append([])
                    driver_row_counter = 1
                    create_entry_row()

        except IndexError:
            pass
        except Exception as e:
            messagebox.showerror("Error Deleting Driver", f"An error occurred while deleting the driver: {e}")

    def load_roster():
        filename = filedialog.askopenfilename(defaultextension=".csv",
                                              filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                              title="Load Roster")
        if filename:
            try:
                event_data, roster_data = dh.load_roster_data(filename)

                # Clear existing data in the Treeview
                tree.delete(*tree.get_children())

                # Clear existing entry widgets and list
                for row in driver_entries:
                    for widget in row:
                        widget.grid_forget()
                        widget.destroy()
                driver_entries.clear()

                nonlocal driver_row_counter
                driver_row_counter = 1
                driver_entries.append([])

                # Recreate entry row with correct Timezone options
                for col_num, col_name in enumerate(column_names):
                    var = None
                    entry = None
                    if col_name in ["Back to Back Stints", "Triple Stint", "Start", "Finish"]:
                        var = tk.BooleanVar()
                        entry = ttk.Checkbutton(entry_frame, variable=var)
                        entry.var = var
                    elif col_name == "Timezone":
                        var = tk.StringVar(value=list(timezone_mapping.keys())[0]) #set the default value to the first key in the dict
                        entry = ttk.Combobox(entry_frame, textvariable=var, values=list(timezone_mapping.keys())) # Use timezone_mapping keys
                        entry.var = var
                    else:
                        entry = ttk.Entry(entry_frame)
                    driver_entries[-1].append(entry)
                    if entry:
                        entry.grid(row=0, column=col_num, padx=5, pady=2, sticky="ew")

                # Populate Event Info (same as before)
                for i, entry in enumerate(event_entries):
                    entry.delete(0, tk.END)
                    if i < len(event_data):
                        entry.insert(0, event_data[i])

                # Populate Driver Table (Corrected Timezone Handling)
                for row_data in roster_data:
                    new_row = []
                    for i, value in enumerate(row_data):
                        if column_names[i] == "Timezone":
                            # Check if the loaded timezone is a valid key in timezone_mapping
                            if value in timezone_mapping.values():
                                # Find the key corresponding to the value
                                key = list(timezone_mapping.keys())[list(timezone_mapping.values()).index(value)]
                                new_row.append(key)
                            else:
                                new_row.append("UTC")  # Default to UTC if not found
                        else:
                            new_row.append(value)
                    tree.insert("", tk.END, values=new_row)

            except FileNotFoundError:
                messagebox.showerror("Error Loading Roster", "File not found.")
            except IndexError:
                messagebox.showerror("Error Loading Roster", "The selected file is not in the correct format.")
            except Exception as e:
                messagebox.showerror("Error Loading Roster", f"An error occurred while loading the roster: {e}")
        else:
            messagebox.showinfo("Load Cancelled", "Load was cancelled")


    icon = tk.PhotoImage(file='racing_flag_PNG.png')
    roster_window = tk.Toplevel(master)
    roster_window.title("Team Roster")
    roster_window.iconphoto(False, icon)
    roster_window.resizable(False, False)
    roster_window.configure(bg='#3d3d3d')
    center_window(roster_window, 650, 630)

    # Static Event Info
    event_frame = ttk.LabelFrame(roster_window, text="Event Information")
    event_frame.grid(row= 0, column= 0, sticky='ew', padx=10, pady=10)
    roster_window.columnconfigure(0, weight=1)

    event_labels = ["Event Name:", "Team Name:", "Track:", "Car:", "Race Length:"]
    event_entries = []
    for i, label_text in enumerate(event_labels):
        ttk.Label(event_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        entry = ttk.Entry(event_frame)
        entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
        event_entries.append(entry)

    # Driver Table
    driver_frame = ttk.LabelFrame(roster_window, text="Driver Roster")
    driver_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    roster_window.rowconfigure(1, weight=1)



    column_names = ["iRating", "Driver Name", "Back to Back Stints", "Triple Stint", "Timezone", "Start", "Finish"]

    # Create the entry frame
    entry_frame = ttk.Frame(driver_frame)
    entry_frame.grid(row=2, column=0, columnspan=len(column_names), sticky="nsew")

    tree = ttk.Treeview(driver_frame, columns=column_names, show="headings")

    # Configure column widths
    tree.column("iRating", width=50)  # Reduced width
    tree.column("Driver Name", width=150)  # Increased width
    tree.column("Back to Back Stints", width=100)
    tree.column("Triple Stint", width=75)
    tree.column("Timezone", width=75)
    tree.column("Start", width=50)
    tree.column("Finish", width=50)

    for col in column_names:
        tree.heading(col, text=col)

    tree.grid(row=0, column=0, columnspan=len(column_names), sticky="nsew")
    tree.bind("<Button-3>", delete_driver)  # Bind right click to the treeview

    driver_row_counter = 1
    driver_entries = []
    driver_entries.append([])

    create_entry_row()

    # Create LABELS ONLY here
    for col_num, col_name in enumerate(column_names):
        ttk.Label(driver_frame, text=col_name).grid(row=1, column=col_num, padx=5, pady=2,
                                                    sticky="w")  # Labels are now on row 1


    add_driver_button = ttk.Button(driver_frame, text="Add Driver", command=add_driver)
    add_driver_button.grid(row=driver_row_counter + 2, columnspan=len(column_names), sticky='nsew')

    save_button = ttk.Button(roster_window, text="Save", command=save_roster)
    save_button.grid(row= driver_row_counter + 4, column= 0, sticky='ew', padx=10, pady=10)

    load_button = ttk.Button(roster_window, text="Load Roster", command=load_roster)
    load_button.grid(row=driver_row_counter + 5, column=0, columnspan=len(column_names), sticky='ew', padx=10, pady=10)
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from roster_window import open_team_roster
import driver_avail

class AppButton:
    def __init__(self, master, text, label_text, command=None):
        self.master = master
        self.text = text
        self.label_text = label_text
        self.command = command

        self.button = ttk.Button(master, text=self.text, command=self.command)
        self.label = ttk.Label(master, text=self.label_text)

    def grid(self, row, button_column=0, label_column=1, sticky='nsew', padx=5, pady=20):
        self.button.grid(row=row, column=button_column, sticky=sticky, padx=padx, pady=pady)
        self.label.grid(row=row, column=label_column, sticky='w', padx=padx, pady=pady)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

root = ThemedTk(theme='equilux')
style = ttk.Style(root)
style.theme_use('equilux')

root.configure(bg='#3d3d3d')

icon = tk.PhotoImage(file='racing_flag_PNG.png')
root.title("CheckeredFlagSimCalc")
root.iconphoto(False, icon)

root.resizable(False, False)
center_window(root, 900, 500)

title_label = ttk.Label(root, text="Checkered Flag Sim Racing Calculator", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20)) # Span across columns, add padding

num_rows = 4
num_cols = 2

version_label = ttk.Label(root, text="Version 0.1 - © 2025 J.R. McDonald II")
version_label.grid(row=num_rows + 1, column=0, columnspan=2, pady=(10, 0)) # Place below buttons

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
for row in range(num_rows+2):
    root.rowconfigure(row, weight=1)

button_data = [
    {"text": "Team Roster", 'label': 'Opens the team roster window', 'command': lambda: open_team_roster(root)},
    {"text": "Driver Availability", 'label': 'Opens the driver availability window', 'command': lambda: driver_avail.open_availability_window(root)},
    {"text": "Driver Statistics", 'label': 'Opens the driver statistics window'},
    {'text': 'Calculate Race Schedule', 'label': 'Calculate Race Schedule'},
]

buttons = []

row_num = 1
for data in button_data:
    button = AppButton(root, data['text'], data['label'], data.get('command'))
    button.grid(row=row_num)
    buttons.append(button)
    row_num += 1

if __name__ == '__main__':
    root.mainloop()
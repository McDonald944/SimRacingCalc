import csv

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
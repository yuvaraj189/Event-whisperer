import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
import pyttsx3

# Connect to SQLite database
conn = sqlite3.connect('events.db')
c = conn.cursor()

# Create events table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS events
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              date DATE,
              time TIME,
              location TEXT,
              description TEXT)''')
conn.commit()

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def add_event(title, date, time, location, description):
    c.execute('''INSERT INTO events (title, date, time, location, description)
                 VALUES (?, ?, ?, ?, ?)''', (title, date, time, location, description))
    conn.commit()

def view_events():
    c.execute('''SELECT * FROM events ORDER BY date, time''')
    events = c.fetchall()
    if events:
        event_list = "\n".join([f"{event[1]} on {event[2]} at {event[3]} at {event[4]}. {event[5]}" for event in events])
        messagebox.showinfo("Upcoming Events", event_list)
        speak("Here are the upcoming events.")
        speak(event_list)
    else:
        messagebox.showinfo("Upcoming Events", "No upcoming events.")
        speak("There are no upcoming events.")

def search_events(year, month, day):
    search_date = datetime(year, month, day)
    c.execute('''SELECT * FROM events WHERE date = ? ORDER BY time''', (search_date.strftime('%Y-%m-%d'),))
    events = c.fetchall()
    if events:
        event_list = "\n".join([f"{event[1]} at {event[3]} at {event[4]}. {event[5]}" for event in events])
        messagebox.showinfo("Events on " + search_date.strftime('%Y-%m-%d'), event_list)
        speak("Here are the events on " + search_date.strftime('%Y-%m-%d'))
        speak(event_list)
    else:
        messagebox.showinfo("Events on " + search_date.strftime('%Y-%m-%d'), "No events scheduled.")
        speak("There are no events scheduled on " + search_date.strftime('%Y-%m-%d'))

# Create GUI
def create_gui():
    root = tk.Tk()
    root.title("Community Event Manager")
    root.geometry("600x400")  # Set initial window size
    root.configure(bg="#D3D3D3")  # Set background color to neon green

    def add_event_callback():
        add_event_frame.grid(row=8, column=0, columnspan=3)
        add_event_button.grid_forget()
        search_events_button.grid_forget()
        view_events_button.grid_forget()

    def confirm_add_event():
        # Retrieve event details from input fields
        title = title_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        location = location_entry.get()
        description = description_entry.get()

        # Add event to the database
        add_event(title, date, time, location, description)
        messagebox.showinfo("Success", "Event added successfully.")
        add_event_frame.grid_forget()
        add_event_button.grid(row=8, column=0, columnspan=3)
        search_events_button.grid(row=3, column=0, columnspan=3)
        view_events_button.grid(row=4, column=0, columnspan=3)

    def view_events_callback():
        view_events()

    def search_events_callback():
        year = int(year_entry.get())
        month = int(month_entry.get())
        day = int(day_entry.get())
        search_events(year, month, day)

    # Labels and entry fields for searching events
    tk.Label(root, text="Year:", bg="#00FF00").grid(row=0, column=0)
    tk.Label(root, text="Month (1-12):", bg="#00FF00").grid(row=0, column=1)
    tk.Label(root, text="Day:", bg="#00FF00").grid(row=0, column=2)
    year_entry = tk.Entry(root)
    month_entry = tk.Entry(root)
    day_entry = tk.Entry(root)
    year_entry.grid(row=1, column=0)
    month_entry.grid(row=1, column=1)
    day_entry.grid(row=1, column=2)

    # Button to search events
    search_events_button = tk.Button(root, text="Search Events", command=search_events_callback, bg="#FFFF00")  # Set button color to neon yellow
    search_events_button.grid(row=3, column=0, columnspan=3)

    # Button to add event
    add_event_button = tk.Button(root, text="Add Event", command=add_event_callback, bg="#FF00FF")  # Set button color to neon pink
    add_event_button.grid(row=4, column=0, columnspan=3)

    # Button to view upcoming events
    view_events_button = tk.Button(root, text="View Upcoming Events", command=view_events_callback, bg="#00FFFF")  # Set button color to neon cyan
    view_events_button.grid(row=5, column=0, columnspan=3)

    # Frame for adding events (initially hidden)
    add_event_frame = tk.Frame(root, bg="#00FF00")  # Set frame color to neon green
    add_event_frame.grid(row=8, column=0, columnspan=3)
    add_event_frame.grid_forget()  # Initially hidden

    # Entry fields for adding events
    tk.Label(add_event_frame, text="Title:", bg="#00FF00").grid(row=0, column=0)
    tk.Label(add_event_frame, text="Date (YYYY-MM-DD):", bg="#00FF00").grid(row=1, column=0)
    tk.Label(add_event_frame, text="Time (HH:MM):", bg="#00FF00").grid(row=2, column=0)
    tk.Label(add_event_frame, text="Location:", bg="#00FF00").grid(row=3, column=0)
    tk.Label(add_event_frame, text="Description:", bg="#00FF00").grid(row=4, column=0)

    title_entry = tk.Entry(add_event_frame)
    date_entry = tk.Entry(add_event_frame)
    time_entry = tk.Entry(add_event_frame)
    location_entry = tk.Entry(add_event_frame)
    description_entry = tk.Entry(add_event_frame)

    title_entry.grid(row=0, column=1)
    date_entry.grid(row=1, column=1)
    time_entry.grid(row=2, column=1)
    location_entry.grid(row=3, column=1)
    description_entry.grid(row=4, column=1)

    # Button to confirm adding event
    add_event_confirm_button = tk.Button(add_event_frame, text="Confirm Add Event", command=confirm_add_event, bg="#00FF00")  # Set button color to neon green
    add_event_confirm_button.grid(row=5, column=0, columnspan=2)

    root.mainloop()

# Sample usage
add_event("Community Meeting", "2024-03-04", "18:00", "Community Center", "Monthly meeting to discuss community issues")
add_event("Volunteer Cleanup", "2024-03-20", "09:00", "Local Park", "Volunteer event to clean up the park")

# Create GUI
create_gui()

# Close database connection
conn.close()
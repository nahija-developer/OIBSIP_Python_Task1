import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

# CSV file to store data
DATA_FILE = "bmi_data.csv"

# Create file with headers if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Weight", "Height", "BMI", "Category"])

# BMI calculation logic
def calculate_bmi():
    name = name_entry.get().strip()
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter numeric values for weight and height.")
        return

    if not name:
        messagebox.showerror("Missing name", "Please enter your name.")
        return
    
    if height <= 0 or weight <= 0:
        messagebox.showerror("Invalid input", "Weight and height must be positive numbers.")
        return

    bmi = weight / (height ** 2)
    bmi = round(bmi, 2)

    # Determine category
    if bmi < 16:
        category = "Severely underweight"
    elif 16 <= bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Healthy"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    result_label.config(text=f"BMI: {bmi} ({category})")

    # Save to CSV
    with open(DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, bmi, category])

    messagebox.showinfo("Saved", "BMI data saved successfully!")

# View history
def view_history():
    history_win = tk.Toplevel(root)
    history_win.title("BMI History")

    with open(DATA_FILE, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        tk.Label(history_win, text="No data available.").pack()
        return

    for row in rows:
        tk.Label(history_win, text=", ".join(row)).pack()

# Plot BMI trend
def show_trend():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Missing name", "Enter your name to view your BMI trend.")
        return

    dates = []
    bmis = []

    with open(DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Name"].lower() == name.lower():
                dates.append(row["Date"])
                bmis.append(float(row["BMI"]))

    if not dates:
        messagebox.showinfo("No data", f"No data found for {name}.")
        return

    plt.figure(figsize=(8,5))
    plt.plot(dates, bmis, marker='o', linestyle='-', color='blue')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title(f"BMI Trend for {name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main GUI
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Name:").grid(row=0, column=0, pady=5)
tk.Label(root, text="Weight (kg):").grid(row=1, column=0, pady=5)
tk.Label(root, text="Height (m):").grid(row=2, column=0, pady=5)

name_entry = tk.Entry(root)
weight_entry = tk.Entry(root)
height_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
weight_entry.grid(row=1, column=1)
height_entry.grid(row=2, column=1)

tk.Button(root, text="Calculate BMI", command=calculate_bmi).grid(row=3, column=0, columnspan=2, pady=10)
result_label = tk.Label(root, text="BMI: ")
result_label.grid(row=4, column=0, columnspan=2)

tk.Button(root, text="View History", command=view_history).grid(row=5, column=0, pady=5)
tk.Button(root, text="Show BMI Trend", command=show_trend).grid(row=5, column=1, pady=5)

root.mainloop()

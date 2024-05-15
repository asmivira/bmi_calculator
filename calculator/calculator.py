import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_bmi(weight, height):
    """
    Calculate BMI (Body Mass Index) using weight (in kilograms) and height (in meters).
    BMI = weight / (height * height)
    """
    return weight / (height ** 2)

def save_data(weight, height, bmi):
    """
    Save user data (weight, height, BMI, timestamp) to SQLite database.
    """
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO user_data (weight, height, bmi, timestamp) VALUES (?, ?, ?, ?)",
              (weight, height, bmi, timestamp))
    conn.commit()
    conn.close()
    update_graph()  


def update_graph():
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_data")
    data = c.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("Information", "No data found.")
        return

    timestamps = [row[3] for row in data]
    bmis = [row[2] for row in data]

    ax.clear()  
    ax.plot(timestamps, bmis, marker='o')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('BMI')
    ax.set_title('BMI Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig_canvas.draw()

def calculate_button_clicked():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = calculate_bmi(weight, height)
        bmi_label.config(text=f"BMI: {bmi:.2f}")

        save_data(weight, height, bmi)

        if bmi < 18.5:
            category_label.config(text="Underweight")
        elif 18.5 <= bmi < 25:
            category_label.config(text="Normal weight")
        elif 25 <= bmi < 30:
            category_label.config(text="Overweight")
        else:
            category_label.config(text="Obese")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid weight and height.")

conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_data
             (weight REAL, height REAL, bmi REAL, timestamp TEXT)''')
conn.commit()
conn.close()

root = tk.Tk()
root.title("BMI Calculator")

weight_label = tk.Label(root, text="Weight (kg):", font=("Arial", 30))
weight_label.pack()
weight_entry = tk.Entry(root, font=("Arial", 30))
weight_entry.pack()

height_label = tk.Label(root, text="Height (m):", font=("Arial", 30))
height_label.pack()
height_entry = tk.Entry(root, font=("Arial", 30))
height_entry.pack()

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_button_clicked, font=("Arial", 30))
calculate_button.pack()

bmi_label = tk.Label(root, text="", font=("Arial", 30))
bmi_label.pack()

category_label = tk.Label(root, text="", font=("Arial", 30))
category_label.pack()

fig, ax = plt.subplots()
ax.set_xlabel('Timestamp')
ax.set_ylabel('BMI')
ax.set_title('BMI Trend')
fig_canvas = FigureCanvasTkAgg(fig, master=root)
fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

view_history_button = tk.Button(root, text="View History", command=update_graph, font=("Arial", 30))
view_history_button.pack()

root.mainloop()

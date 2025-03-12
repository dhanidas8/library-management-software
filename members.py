import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="librarydb"
)
cursor = conn.cursor()

# Function to add a new member
def add_member():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    if name and email and phone:
        try:
            query = "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, phone))
            conn.commit()
            messagebox.showinfo("Success", "Member added successfully!")
            display_members()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

# Function to display members in the table
def display_members():
    for row in tree.get_children():
        tree.delete(row)
    
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

# GUI Setup
root = tk.Tk()
root.title("Library Management - Members")

# Labels and Entry Fields
tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Email").grid(row=1, column=0)
tk.Label(root, text="Phone").grid(row=2, column=0)

name_entry = tk.Entry(root)
email_entry = tk.Entry(root)
phone_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
email_entry.grid(row=1, column=1)
phone_entry.grid(row=2, column=1)

# Buttons
tk.Button(root, text="Add Member", command=add_member).grid(row=3, column=1)

# Table for displaying members
tree = ttk.Treeview(root, columns=("ID", "Name", "Email", "Phone"), show="headings")
tree.heading("ID", text="Member ID")
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")

tree.grid(row=4, column=0, columnspan=2)
display_members()

root.mainloop()

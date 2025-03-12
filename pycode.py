import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# MySQL connection setup
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='library',
            user='root',
            password='password'  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Add student function
def add_student():
    name = student_name_entry.get()
    email = student_email_entry.get()
    connection = connect_db()
    cursor = connection.cursor()
    query = "INSERT INTO students (name, email) VALUES (%s, %s)"
    cursor.execute(query, (name, email))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Student added successfully!")

# Add book function
def add_book():
    title = book_title_entry.get()
    author = book_author_entry.get()
    connection = connect_db()
    cursor = connection.cursor()
    query = "INSERT INTO books (title, author) VALUES (%s, %s)"
    cursor.execute(query, (title, author))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Book added successfully!")

# Issue book function
def issue_book():
    student_id = student_id_entry.get()
    book_id = book_id_entry.get()
    issue_date = issue_date_entry.get()
    connection = connect_db()
    cursor = connection.cursor()
    query = "INSERT INTO transactions (student_id, book_id, issue_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (student_id, book_id, issue_date))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Book issued successfully!")

# Return book function
def return_book():
    transaction_id = transaction_id_entry.get()
    return_date = return_date_entry.get()
    connection = connect_db()
    cursor = connection.cursor()
    query = "UPDATE transactions SET return_date = %s WHERE transaction_id = %s"
    cursor.execute(query, (return_date, transaction_id))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Book returned successfully!")

# Tkinter GUI
root = tk.Tk()
root.title("Library Management System")

# Student Section
tk.Label(root, text="Student Name:").grid(row=0, column=0)
student_name_entry = tk.Entry(root)
student_name_entry.grid(row=0, column=1)

tk.Label(root, text="Student Email:").grid(row=1, column=0)
student_email_entry = tk.Entry(root)
student_email_entry.grid(row=1, column=1)

tk.Button(root, text="Add Student", command=add_student).grid(row=2, column=0, columnspan=2)

# Book Section
tk.Label(root, text="Book Title:").grid(row=3, column=0)
book_title_entry = tk.Entry(root)
book_title_entry.grid(row=3, column=1)

tk.Label(root, text="Book Author:").grid(row=4, column=0)
book_author_entry = tk.Entry(root)
book_author_entry.grid(row=4, column=1)

tk.Button(root, text="Add Book", command=add_book).grid(row=5, column=0, columnspan=2)

# Issue Book Section
tk.Label(root, text="Student ID:").grid(row=6, column=0)
student_id_entry = tk.Entry(root)
student_id_entry.grid(row=6, column=1)

tk.Label(root, text="Book ID:").grid(row=7, column=0)
book_id_entry = tk.Entry(root)
book_id_entry.grid(row=7, column=1)

tk.Label(root, text="Issue Date (YYYY-MM-DD):").grid(row=8, column=0)
issue_date_entry = tk.Entry(root)
issue_date_entry.grid(row=8, column=1)

tk.Button(root, text="Issue Book", command=issue_book).grid(row=9, column=0, columnspan=2)

# Return Book Section
tk.Label(root, text="Transaction ID:").grid(row=10, column=0)
transaction_id_entry = tk.Entry(root)
transaction_id_entry.grid(row=10, column=1)

tk.Label(root, text="Return Date (YYYY-MM-DD):").grid(row=11, column=0)
return_date_entry = tk.Entry(root)
return_date_entry.grid(row=11, column=1)

tk.Button(root, text="Return Book", command=return_book).grid(row=12, column=0, columnspan=2)

root.mainloop()

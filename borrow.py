import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="librarydb"
)
cursor = conn.cursor()

# Function to Issue a Book
def issue_book():
    member_id = member_id_entry.get()
    book_id = book_id_entry.get()

    if member_id and book_id:
        try:
            # Check if book exists and is available
            cursor.execute("SELECT available FROM books WHERE book_id = %s", (book_id,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Invalid Book ID!")
                return
            
            available_copies = result[0]
            if available_copies > 0:
                # Issue the book
                cursor.execute("INSERT INTO book_issuance (member_id, book_id) VALUES (%s, %s)", (member_id, book_id))
                
                # Update book availability
                cursor.execute("UPDATE books SET available = available - 1 WHERE book_id = %s", (book_id,))
                
                conn.commit()
                messagebox.showinfo("Success", "Book issued successfully!")
                display_issued_books()
            else:
                messagebox.showwarning("Unavailable", "No copies available to issue.")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else:
        messagebox.showwarning("Input Error", "Both Member ID and Book ID are required.")

# Function to Display Issued Books
def display_issued_books():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT issue_id, member_id, book_id, issue_date, return_date FROM book_issuance")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

# GUI Setup
root = tk.Tk()
root.title("Library Management - Issue Books")

# Labels and Entry Fields
tk.Label(root, text="Member ID").grid(row=0, column=0)
tk.Label(root, text="Book ID").grid(row=1, column=0)

member_id_entry = tk.Entry(root)
book_id_entry = tk.Entry(root)

member_id_entry.grid(row=0, column=1)
book_id_entry.grid(row=1, column=1)

# Buttons
tk.Button(root, text="Issue Book", command=issue_book).grid(row=2, column=1)

# Table for displaying issued books
tree = ttk.Treeview(root, columns=("Issue ID", "Member ID", "Book ID", "Issue Date", "Return Date"), show="headings")
tree.heading("Issue ID", text="Issue ID")
tree.heading("Member ID", text="Member ID")
tree.heading("Book ID", text="Book ID")
tree.heading("Issue Date", text="Issue Date")
tree.heading("Return Date", text="Return Date")

tree.grid(row=3, column=0, columnspan=2)
display_issued_books()

root.mainloop()

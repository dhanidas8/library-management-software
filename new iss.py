import mysql.connector
from tkinter import *
from tkinter import ttk
from datetime import date, timedelta

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="librarydb"
)
cursor = conn.cursor()

# Create Tkinter Window
root = Tk()
root.title("Library Management - Issue & Return Books")

# Labels and Inputs
Label(root, text="Member ID:").grid(row=0, column=0)
member_entry = Entry(root)
member_entry.grid(row=0, column=1)

Label(root, text="Book ID:").grid(row=1, column=0)
book_entry = Entry(root)
book_entry.grid(row=1, column=1)

# Treeview (Table)
columns = ("Issue ID", "Member ID", "Book ID", "Issue Date", "Return Date", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.grid(row=3, column=0, columnspan=3, pady=10)

# Function to Load Data
def load_data():
    tree.delete(*tree.get_children())  # Clear Table
    cursor.execute("SELECT issue_id, member_id, book_id, issue_date, return_date, is_returned FROM book_issuance")
    for row in cursor.fetchall():
        status = "Returned" if row[5] else "Issued"
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], status))

# Function to Issue Book
def issue_book():
    member_id = member_entry.get()
    book_id = book_entry.get()
    if member_id and book_id:
        issue_date = date.today()  # Get today's date

        cursor.execute("INSERT INTO book_issuance (member_id, book_id, issue_date) VALUES (%s, %s, %s)", 
                       (member_id, book_id, issue_date))  # REMOVE return_date
        conn.commit()
        load_data()


# Function to Return Book
def return_book():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)["values"]
        issue_id = item[0]

        # Update `is_returned` in MySQL
        cursor.execute("UPDATE book_issuance SET is_returned = TRUE WHERE issue_id = %s", (issue_id,))
        conn.commit()

        load_data()

# Buttons
issue_btn = Button(root, text="Issue Book", command=issue_book)
issue_btn.grid(row=2, column=0, pady=5)

return_btn = Button(root, text="Return Book", command=return_book)
return_btn.grid(row=2, column=1, pady=5)

# Load Initial Data
load_data()

# Run Tkinter
root.mainloop()

# Close Connection
conn.close()

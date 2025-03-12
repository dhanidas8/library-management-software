import mysql.connector
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

# Connecting to MySQL Database
connector = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="librarydb"
)
cursor = connector.cursor()

def issuer_card():
    Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?')
    if not Cid:
        mb.showerror('Error', 'Issuer ID cannot be empty')
    return Cid

def display_records():
    tree.delete(*tree.get_children())  # Clear the tree first
    cursor.execute('SELECT * FROM books')
    data = cursor.fetchall()
    for record in data:
        tree.insert('', END, values=record)

def clear_fields():
    bk_name.set("")
    author_name.set("")
    genre.set("")
    available.set(0)  # Default to 0 (unavailable)

def add_record():
    try:
        cursor.execute(
            'INSERT INTO books (title, author, genre, available) VALUES (%s, %s, %s, %s)',
            (bk_name.get(), author_name.get(), genre.get(), available.get())
        )
        connector.commit()
        display_records()
        mb.showinfo('Success', 'Book added successfully')
    except mysql.connector.Error as err:
        mb.showerror('Error', f'Database error: {err}')

def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select a book to delete')
        return
    current_item = tree.focus()
    values = tree.item(current_item)['values']
    cursor.execute('DELETE FROM books WHERE book_id=%s', (values[0],))
    connector.commit()
    tree.delete(current_item)
    mb.showinfo('Success', 'Book deleted')
    display_records()

def change_availability():
    if not tree.selection():
        mb.showerror('Error!', 'Please select a book')
        return
    
    current_item = tree.focus()
    values = tree.item(current_item)['values']
    
    new_status = sd.askinteger("Change Availability", f"Current stock: {values[4]}\nEnter new stock quantity:", minvalue=0)
    
    if new_status is not None:
        cursor.execute('UPDATE books SET available=%s WHERE book_id=%s', (new_status, values[0]))
        connector.commit()
        clear_and_display()
def clear_and_display():
    clear_fields()
    display_records()


# GUI Setup
root = Tk()
root.title('Library Management System')
root.geometry('1010x530')
root.resizable(0, 0)

bk_name = StringVar()
author_name = StringVar()
genre = StringVar()
available = IntVar(value=0)  # Default to 0 (unavailable)

left_frame = Frame(root)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

Label(left_frame, text='Book Name').place(x=98, y=25)
Entry(left_frame, textvariable=bk_name).place(x=45, y=55)
Label(left_frame, text='Author Name').place(x=90, y=185)
Entry(left_frame, textvariable=author_name).place(x=45, y=215)
Label(left_frame, text='Genre').place(x=90, y=245)
Entry(left_frame, textvariable=genre).place(x=45, y=275)
Label(left_frame, text='Available').place(x=90, y=305)
Entry(left_frame, textvariable=available).place(x=45, y=335)

Button(left_frame, text='Add Book', command=add_record).place(x=50, y=375)
Button(left_frame, text='Delete Book', command=remove_record).place(x=50, y=435)
Button(left_frame, text='Change Availability', command=change_availability).place(x=50, y=475)

RB_frame = Frame(root)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

Label(RB_frame, text='BOOK INVENTORY').pack(side=TOP, fill=X)
tree = ttk.Treeview(RB_frame, columns=('Book ID', 'Title', 'Author', 'Genre', 'Available'))

tree.heading('Book ID', text='Book ID')
tree.heading('Title', text='Title')
tree.heading('Author', text='Author')
tree.heading('Genre', text='Genre')
tree.heading('Available', text='Available')

tree.column('Book ID', width=80, anchor=CENTER)
tree.column('Title', width=150, anchor=W)
tree.column('Author', width=120, anchor=W)
tree.column('Genre', width=100, anchor=W)
tree.column('Available', width=80, anchor=CENTER)  # Adjust width for visibility

tree.column('#0', width=0, stretch=NO)  # Hide the default first column
tree.place(y=30, x=0, relheight=0.9, relwidth=1)


display_records()
root.mainloop()

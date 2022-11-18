
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import sqlite3 

root = Tk()
root.title("Contacts")

Connection = sqlite3.connect("contacts.db")

cursor = Connection.cursor()

cursor.execute("""
        CREATE TABLE if not exists contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        company TEXT NOT NULL
        )

""")
def showContacts():
    
    table = cursor.execute("SELECT * FROM contacts").fetchall()

    gridTree.delete(*gridTree.get_children())
    for row in table:
        gridTree.insert('',END, row[0], values=(row[1],row[2],row[3]))


def insert(contact):
    cursor.execute("""
        INSERT INTO contacts (name, phone, company) VALUES (?,?,?)
    
    """, (contact['name'], contact['phone'], contact['company']))
    Connection.commit()
    showContacts()


def new():
    def add():
        if not entryName.get() or not entryPhone.get() or not entryCompany.get():
            messagebox.showerror('Error', 'Todos los campos son obligatorios', parent=top)
            return

        contact = {
        'name': entryName.get(),
        'phone': entryPhone.get(),
        'company': entryCompany.get()
        }
        insert(contact)
        top.destroy()


    top = Toplevel()
    top.title('New Contact')

    labelName = Label(top, text='Name')
    entryName = Entry(top, width=40)
    labelName.grid(row=0,column=0)
    entryName.grid(row=0,column=1)

    labelPhone = Label(top,text='Phone')
    entryPhone = Entry(top,width=40)
    labelPhone.grid(row=1, column=0)
    entryPhone.grid(row=1, column=1)

    labelCompany = Label(top,text='Company')
    entryCompany = Entry(top, width=40)
    labelCompany.grid(row=2, column=0)
    entryCompany.grid(row=2,column=1)

    addButton = Button(top, text='Add', command=add)
    addButton.grid(row=3,column=1)
    
    top.mainloop()


def delete():
    id = gridTree.selection()[0]
    calling = cursor.execute("SELECT * FROM contacts where id = ?", (id, )).fetchone()
    asw = messagebox.askyesno('Caution',"Are you sure to delete {} contact from {}?".format(calling[1],calling[3]))
    
    if asw:
        cursor.execute("DELETE FROM contacts WHERE id = ?", (id, ))
        Connection.commit()
        showContacts()
        
    else:
        pass
    

newButton = Button(root, text='New Contact', command= new)
newButton.grid(row=0,column=0)


delButton = Button(root, text='Delete Contact', command= delete)
delButton.grid(row=0, column=1)


gridTree = ttk.Treeview(root)

gridTree['columns'] = ('Name', 'Phone', 'Company')
gridTree.column('#0', width=0,stretch=YES)
gridTree.column('Name')
gridTree.column('Phone')
gridTree.column('Company')

gridTree.heading('Name', text='Name')
gridTree.heading('Phone', text='Phone')
gridTree.heading('Company', text='Company')
gridTree.grid(row=1, column=0, columnspan=2)
showContacts()

root.mainloop()
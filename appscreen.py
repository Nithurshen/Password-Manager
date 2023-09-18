from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import mysql.connector as sql
from mysql.connector import Error

from insertData import InsertData

class MainScreen:
    def __init__(self, root, login_username):
        self.login_username = login_username
        self.root = root
        self.row = []
        root.geometry("1200x700")
        root.title("Passwords Manager")
        root.resizable(width=False, height=False)
        self.row = []
        self.mainFrame = Frame(root, width = 1200, height = 700, bg = "#E9F9CD", bd = 5,relief="ridge",highlightbackground="#ABE1ED", highlightthickness=1)
        self.mainFrame.place(x=0, y=0)
        self.titleFrame = Frame(self.mainFrame, width = 1190, height = 100, bg = "#E9F9CD", relief="flat",highlightbackground="#ABE1ED", highlightthickness=1)
        self.titleFrame.place(x=0, y=0)
        self.heading = Label(self.titleFrame, text = "PASSWORDS MANAGER", font = ("Times New Roman", 35), bg = "#E9F9CD")
        self.heading.place(x=250, y=5)
        self.userLabel = Label(self.titleFrame, text = "Username: " + self.login_username, font = ("Times New Roman", 15), bg = "#E9F9CD")
        self.userLabel.place(x = 400, y=50)
        self.searchFrame = Frame(self.mainFrame, width=390, height = 150, bg ="#E9F9CD", relief="flat",highlightbackground="#ABE1ED", highlightthickness=1)
        self.searchFrame.place(x=800, y=100)
        self.filterFrame = Frame(self.mainFrame, width=800, height = 50, bg ="#E9F9CD", relief="flat",highlightbackground="#ABE1ED", highlightthickness=1)
        self.filterFrame.place(x=0, y=100)
        self.sortbutton = Menubutton(self.filterFrame, text = "Sort", font = ("Times New Roman",15), relief="raised", width = 5,bd = 2)
        self.sortbutton.place(x = 0, y = 10)
        self.sortbutton.menu = Menu(self.sortbutton, tearoff = 0)
        self.sortbutton["menu"] = self.sortbutton.menu
        self.sortbutton.menu.add_command(label = "Ascending", command = lambda: self.displayData("site asc"))
        self.sortbutton.menu.add_command(label = "Descending", command = lambda: self.displayData("site desc"))
        self.sortbutton.menu.add_command(label = "First added", command = lambda: self.displayData("id asc"))
        self.tableFrame = Frame(self.mainFrame, width=800, height = 100, bg ="#E9F9CD", relief="flat",highlightbackground="#ABE1ED", highlightthickness=1)
        self.tableFrame.place(x=0, y=150)
        self.displayButton = Button(self.tableFrame, text = "Show", relief = "raised", font = ("Times New Roman", 15), command = self.displayData)
        self.displayButton.place(x=0, y=50)
        self.dataFrame = Frame(self.mainFrame, width=1190, height = 350, bg ="#E9F9CD", bd = 5, relief="flat")
        self.dataFrame.pack_propagate(0)
        self.dataFrame.place(x=0, y=250)
        self.optionsFrame = Frame(self.mainFrame, width = 1190, height = 100, bg = "#E9F9CD", relief="flat")
        self.optionsFrame.place(x=300, y=600)
        self.scrollerY = Scrollbar(self.dataFrame, orient = VERTICAL)
        self.passwordRecords = ttk.Treeview(self.dataFrame, columns =("site","url","acc_username","acc_password"), height=15, yscrollcommand = self.scrollerY.set)
        self.scrollerY.pack(side = RIGHT, fill = Y)       
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("None", 15))
        self.style.configure("Treeview.Column", font=("None", 15))
        self.passwordRecords.heading("site", text = "Site")
        self.passwordRecords.heading("url", text = "URL")
        self.passwordRecords.heading("acc_username", text = "Username")
        self.passwordRecords.heading("acc_password", text = "Password")
        self.passwordRecords['show'] = 'headings'
        self.passwordRecords.column("site", width=100)
        self.passwordRecords.column("url", width=100)
        self.passwordRecords.column("acc_username", width=100)
        self.passwordRecords.column("acc_password", width=100)
        self.passwordRecords.pack(fill = BOTH, expand = 1)
        self.passwordRecords.bind("<ButtonRelease-1>", self.selectData)
        self.scrollerY.config(command=self.passwordRecords.yview)
        self.displayData()
        self.addButton = Button(self.optionsFrame, text = "Add New", font = ("Times New Roman", 20), command = lambda: self.clicked("addnew"))
        self.addButton.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.deleteButton = Button(self.optionsFrame, text = "Delete", font = ("Times New Roman", 20), command = self.deleteRecord)
        self.deleteButton.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.updateButton = Button(self.optionsFrame, text = "Update", font = ("Times New Roman", 20), command = lambda: self.clicked("update", self.row))
        self.updateButton.grid(row = 1, column = 2, padx = 10, pady = 10)
        self.searchLabel = Label(self.searchFrame, text = "Search Site:",font = ("Times New Roman", 15), bg = "#E9F9CD")
        self.searchLabel.place(x=20, y=10)
        self.searchEntry = Entry(self.searchFrame, font = ("Times New Roman", 15))
        self.searchEntry.place(x=100,y=55)
        self.searchButton = Button(self.searchFrame, text = "Search", font = ("Times New Roman", 15), command = self.searchRecord)
        self.searchButton.place(x=130, y=100)
    def clicked(self, option, row = None):
            if option == "addnew":
                screen = Toplevel(self.root)
                screen.grab_set()
                insert_class = InsertData(screen, self.login_username, option, row, self.displayData)
            if option == "update" and self.row is not None and len(self.row) != 0:
                screen = Toplevel(self.root)
                screen.grab_set()
                insert_class = InsertData(screen, self.login_username, option, row, self.displayData)
            if (option == "update" and len(row) == 0):
                messagebox.showerror("Update Error", "Select Data to Update")
    def selectData(self, ev):
        viewInfo = self.passwordRecords.focus()
        if viewInfo:
            passwordData = self.passwordRecords.item(viewInfo)
            self.row = passwordData['values']
        else:
            self.row = []
    def deleteRecord(self):
        if self.row:
            mydb = None
            try:
                s = self.row[0]
                u = self.row[1]
                usr = self.row[2]
                p = self.row[3]
                mydb = sql.connect(host="localhost", user="root", password="", database="passwords_manager")
                cursor = mydb.cursor()
                cursor.execute("DELETE FROM accounts WHERE username = %s AND url=%s AND acc_username=%s AND acc_password=%s AND site=%s", (self.login_username, u, usr, p, s))
                mydb.commit()
                mydb.close()
                self.displayData()
                self.row = []
            except Error as err:
                print(f"Error: {err}")
        else:
            messagebox.showerror("Delete Error", "Select a Record to Delete")
    def displayData(self, order=None):
        try:
            mydb = sql.connect(host = "localhost", user = "root", password = "", database = "passwords_manager")
            cursor = mydb.cursor()
            if order:
                cursor.execute("SELECT site,url,acc_username,acc_password FROM accounts WHERE username = %s ORDER BY " + order, (self.login_username,))
            else:
                cursor.execute("SELECT site,url,acc_username,acc_password FROM accounts WHERE username = %s", (self.login_username,))
            results = cursor.fetchall()
            for item in self.passwordRecords.get_children():
                self.passwordRecords.delete(item)
            for row in results:
                self.passwordRecords.insert('', END, values = row)
                mydb.commit()
        except Error as err:
            print(f"Error: {err}")
        finally:
            mydb.close()
    def searchRecord(self):
        value = self.searchEntry.get()
        if(len(value)>=1):
            try:
                mydb = sql.connect(host = "localhost", user = "root", password = "", database = "passwords_manager")
                cursor = mydb.cursor()
                cursor.execute("SELECT site,url,acc_username,acc_password FROM accounts WHERE username = %s AND site LIKE %s", (self.login_username, value + "%",))
                results = cursor.fetchall()
                if(not results):
                    messagebox.showerror("Error", value + " not found")
                else:
                    self.passwordRecords.selection()
                    fetchdata = self.passwordRecords.get_children()
                    for f in fetchdata:
                        self.passwordRecords.delete(f)
                    for res in results:
                        self.passwordRecords.insert("", END, values=res)
            except Error as err:
                print(f"Error: {err}")
            finally:
                mydb.close()

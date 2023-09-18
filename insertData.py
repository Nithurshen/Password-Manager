from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import mysql.connector as sql
from mysql.connector import Error

class InsertData:
    def __init__(self, root, login_username, option, row, display):
        self.display = display
        self.row = row
        self.option = option
        self.root = root
        self.login_username = login_username
        root.title("Add Record")
        root.geometry("400x270")
        root.resizable(width=False, height=False)
        self.headingLabel = Label(root, text = "Enter Record",font = ("Times New Roman", 20))
        self.headingLabel.pack()
        self.intro = Label(root, text = "Enter Details You Want To Update",font = ("Times New Roman", 15))
        self.intro.pack()
        self.titleFrame = Frame(root, width = 400)
        self.titleFrame.pack()
        self.mainFrame1 = Frame(root, width = 400)
        self.mainFrame1.pack()
        self.siteLabel = Label(self.mainFrame1, text = "Site:",font = ("Times New Roman", 15))
        self.siteLabel.grid(sticky = "W", row=0, column=0)
        self.urlLabel = Label(self.mainFrame1, text = "URL:",font = ("Times New Roman", 15))
        self.urlLabel.grid(sticky = "W", row=1, column=0)
        self.passwordLabel = Label(self.mainFrame1, text = "Password:",font = ("Times New Roman", 15))
        self.passwordLabel.grid(sticky = "W", row=2, column=0)
        self.usernameLabel = Label(self.mainFrame1, text = "Username:",font = ("Times New Roman", 15))
        self.usernameLabel.grid(sticky = "W", row=3, column=0)
        self.siteEntry = Entry(self.mainFrame1, font = ("Times New Roman", 15))
        self.siteEntry.grid(row=0, column=1)
        self.urlEntry = Entry(self.mainFrame1, font = ("Times New Roman", 15))
        self.urlEntry.grid(row=1, column=1)
        self.passwordEntry = Entry(self.mainFrame1, font = ("Times New Roman", 15))
        self.passwordEntry.grid(row=2, column=1)
        self.usernameEntry = Entry(self.mainFrame1, font = ("Times New Roman", 15))
        self.usernameEntry.grid(row=3, column=1)
        self.buttonsFrame = Frame(root, width = 400)
        self.buttonsFrame.pack()
        self.addRecordButton = Button(self.buttonsFrame, text = "Go", font = ("Times New Roman", 15), command = lambda: self.clickedButton(self.option, self.row))
        self.addRecordButton.grid(row=0, column=0, padx = 10, pady = 10)
        self.resetButton = Button(self.buttonsFrame, text = "Reset", font = ("Times New Roman", 15), command = self.resetEntry)
        self.resetButton.grid(row=0, column=1, padx = 10, pady = 10)        
    def close(self):
        self.root.destroy()
    def resetEntry(self):
        self.siteEntry.delete(0, END)
        self.urlEntry.delete(0, END)
        self.passwordEntry.delete(0, END)
        self.usernameEntry.delete(0, END)
    def clickedButton(self, option, row = None):
        if(len(self.siteEntry.get().split()) == 0 or len(self.passwordEntry.get().split())==0 or len(self.usernameEntry.get().split())==0 or len(self.urlEntry.get().split())==0): 
            messagebox.showerror("Update", "No Field Can Be Empty")
        else:
            try:
                mydb = sql.connect(host = "localhost", user = "root", password = "", database = "passwords_manager")
                cursor = mydb.cursor()
                if(option == "addnew"):
                    cursor.execute("INSERT INTO accounts (username,site,url,acc_username,acc_password) VALUES(%s, %s, %s, %s, %s)", (self.login_username, self.siteEntry.get(),self.urlEntry.get(),self.usernameEntry.get(),self.passwordEntry.get()))
                if(option == "update"): 
                    cursor.execute("UPDATE accounts SET url=%s, acc_username=%s, acc_password=%s, site=%s WHERE username = %s AND url=%s AND acc_username=%s AND acc_password=%s AND site=%s",(self.urlEntry.get(), self.usernameEntry.get(),self.passwordEntry.get(),self.siteEntry.get(),self.login_username,row[1],row[2],row[3],row[0]))
                mydb.commit()
                self.close()
                self.root.grab_release()
                run = self.display()
            except Error as err:
                print(f"Error: {err}")
            finally:
                mydb.close()

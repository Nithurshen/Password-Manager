from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import mysql.connector as sql
from mysql.connector import Error

from createAccount import CreateAccount
from appscreen import MainScreen

class LoginScreen:
    def __init__(self, root):
        self.root = root
        root.geometry("600x500")
        root.title("Login")
        root.resizable(width=False, height=False)
        mainFrame = Frame(root, width = 600, height = 500, bg = "#E9F9CD")
        mainFrame.pack()
        self.heading = Label(mainFrame, text="LOGIN", font = ("Times New Roman", 35), bg = "#E9F9CD")
        self.heading.place(x = 200, y = 150)
        self.username_label = Label(root, text="Username: ", font = ("Times New Roman", 16), bg = "#E9F9CD")
        self.username_label.place(x= 100, y= 280)
        self.password_label = Label(root, text="Password: ", font = ("Times New Roman", 16), bg = "#E9F9CD")
        self.password_label.place(x = 100, y= 330)
        self.username_entry = Entry(root, font = ("Times New Roman", 16))
        self.username_entry.place(x = 200, y= 280)
        self.password_entry = Entry(root, font = ("Times New Roman", 16), show = "*")
        self.password_entry.place(x= 200,y= 330)
        self.submit_button = Button(root, text="Login", font = ("Times New Roman", 16), width = 18, command = self.login)
        self.submit_button.place(x=200, y=380)
        self.signup_button = Button(root, text="Create Account", font = ("Times New Roman", 16), width = 18, command = self.callCreate)
        self.signup_button.place(x= 200, y=430)
    def callCreate(self):
        rt = Tk()
        cs = CreateAccount(rt, self.root) 
        self.close()
    def callApp(self, usern):
        rt = Tk()
        c = MainScreen(rt, usern)
        self.close()
    def close(self):
        self.root.destroy()
    def login(self):
        if(self.username_entry.get() == "" or self.password_entry.get() == ""):
            messagebox.showerror("Login", "Enter Your Login")
        else:
            mydb = None
            try:
                mydb = sql.connect(host = "localhost", user = "root", password = "", database = "passwords_manager")
                cursor = mydb.cursor()
                cursor.execute("SELECT username, password FROM users WHERE username = %s and password = %s",(self.username_entry.get(), self.password_entry.get()))
                results = cursor.fetchone()
                if(results == None):
                    messagebox.showerror("Login Error", "Logins Not Found")
                else:
                    login_username = self.username_entry.get()
                    self.callApp(login_username)
            except Error as err:
                print(f"Error: {err}")
                
root = Tk()

ls = LoginScreen(root)

root.mainloop()

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import mysql.connector as sql
from mysql.connector import Error

from appscreen import MainScreen

class CreateAccount:
    def __init__(self, root, login_screen):
        self.root = root
        self.login_screen = login_screen      
        root.geometry("600x400")
        root.title("Create Account")
        root.resizable(width=False, height=False)
        mainFrame = Frame(root, width = 600, height = 500, bg = "#E9F9CD")
        mainFrame.pack()
        self.heading = Label(mainFrame, text="CREATE ACCOUNT", font=("Times New Roman", 30), bg = "#E9F9CD")
        self.heading.place(x=150, y=30)
        self.username_label = tk.Label(mainFrame, text="Username:", font=("Times New Roman", 16), bg = "#E9F9CD")
        self.username_label.place(x=50 ,y=100)
        self.password_label = tk.Label(mainFrame, text="Password:", font=("Times New Roman", 16), bg = "#E9F9CD")
        self.password_label.place(x=50 ,y=150)
        self.confirmp_label = tk.Label(mainFrame, text="Confirm Password:", font=("Times New Roman", 16), bg = "#E9F9CD")
        self.confirmp_label.place(x=50 ,y=200)
        self.username_entry = tk.Entry(mainFrame,font = ("Times New Roman", 15))
        self.username_entry.place(x=250 ,y=100)
        self.password_entry = tk.Entry(mainFrame,font = ("Times New Roman", 15), show="*")
        self.password_entry.place(x=250 ,y=150)
        self.confirmp_entry = tk.Entry(mainFrame,font = ("Times New Roman", 15), show="*")
        self.confirmp_entry.place(x=250 ,y=200)
        self.signup_button = Button(mainFrame, text="Submit", font=("Times New Roman", 16), command = self.submit)
        self.signup_button.place(x=200, y=300)
        self.clear_button = Button(mainFrame, text="Clear", font=("Times New Roman", 16), command = self.clear)
        self.clear_button.place(x=300, y=300)        
    def clear(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.confirmp_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.recovery_q_entry.delete(0, END)
        self.recovery_a_entry.delete(0, END)
    def close(self):
        self.root.destroy()    
    def callApp(self, usern):
        rt = Tk()
        c = MainScreen(rt, usern)
        self.close()
    def submit(self):
        if(len(self.username_entry.get()) < 6 or len(self.password_entry.get())<8 or self.confirmp_entry.get() == "" or(self.password_entry.get() != self.confirmp_entry.get())):
            messagebox.showerror("details", "Enter your details")
        else:
            try:
                mydb = sql.connect(host = "localhost", user = "root", password = "", database = "passwords_manager")
                cursor = mydb.cursor()
                cursor.execute("SELECT username from users WHERE username = %s", (self.username_entry.get(),))
                usernames = cursor.fetchone()
                if(usernames != None):
                    messagebox.showerror("Create Account", "Username Already Exists")
                else:
                    cursor.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (self.username_entry.get(), self.password_entry.get()))
                    mydb.commit()
                    login_username = self.username_entry.get()
                    self.callApp(login_username)


            except Error as err:
                print(f"Error: {err}")

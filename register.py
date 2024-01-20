import tkinter as tk
from dotenv import load_dotenv,find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())

password=os.environ.get("MONGODB_PWD")
connection_string=f"mongodb+srv://mk_18:{password}@mk18cluster.3ejfo1y.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(connection_string)

dbs=client.list_database_names()
database=client.AML_2048
collections=database.list_collection_names()
collection=database.User_Info

def insert_userinfo(userid,password):
    user_doc={
        "UserName": userid,
        "Password": password
    }
    insertedDoc=collection.insert_one(user_doc)
    id=insertedDoc.inserted_id
    #print(id)

class RegistrationForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        #self.master = master
        self.title("Registration Form")
        self.geometry("800x600")
       
        #create a frame to center the fields
        self.frame = tk.Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # create labels and entry fields for username, password, and confirm password
        self.username_label = tk.Label(self.frame, text="Username:", anchor="center")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.frame, text="Password:",anchor="center")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.confirm_password_label = tk.Label(self.frame, text="Confirm Password:",anchor="center")
        self.confirm_password_label.grid(row=2, column=0, padx=10, pady=10)

        self.confirm_password_entry = tk.Entry(self.frame, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=10)

        # create a button to submit the registration form
        self.register_button = tk.Button(self.frame, text="Register", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=20)

        # create a label to display any error messages
        self.error_label = tk.Label(self.frame, fg="red", text = "")
        self.error_label.grid(row=4, column=0, columnspan=2)

        # create a label to display a success message after registration
        self.success_label = tk.Label(self.frame, fg="green", text = "")
        self.success_label.grid(row=5, column=0, columnspan=2)

    def register(self):
        username = self.username_entry.get()
        userfound=collection.find_one({"UserName":username})
        if userfound!=None:
            self.error_label.config(text="User Name already exist.")
        else:
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
     # validate the registration form and display error or success messages
        if not username:
            self.error_label.config(text="Please enter a username.")
        elif not password:
            self.error_label.config(text="Please enter a password.")
        elif password != confirm_password:
            self.error_label.config(text="Passwords do not match.")
        elif username!=None and password==confirm_password:
            insert_userinfo(username,password)
            self.error_label.config(text="")
            self.success_label.config(text="Registration successful.")

'''
# set the window size and center it on the screen
        width = 500
        height = 400
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")
'''
import tkinter as tk
from dotenv import load_dotenv,find_dotenv
import os
import pprint
from Game import Game2048
from pymongo import MongoClient
load_dotenv(find_dotenv())

password=os.environ.get("MONGODB_PWD")
connection_string=f"mongodb+srv://mk_18:{password}@mk18cluster.3ejfo1y.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(connection_string)

dbs=client.list_database_names()
database=client.AML_2048
collections=database.list_collection_names()
collection=database.User_Info

class LoginPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        #self.master = master
        self.title("Login Page")
        self.geometry("800x600")

        # Create the login frame and center it in the window
        self.login_frame = tk.Frame(self)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create the username label and entry field
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create the password label and entry field
        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create the login button
        self.login_button = tk.Button(self.login_frame, text="Login", width=10, command=self.validate_login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Create the error label
        self.error_label = tk.Label(self.login_frame, text="", fg="red")
        self.error_label.grid(row=4, column=0, columnspan=2)

    def validate_login(self):
        # Get the values entered in the username and password fields
        username = self.username_entry.get()
        password = self.password_entry.get()
        userfound=collection.find_one({"UserName":username})
        usr=str(userfound['UserName'])
        # Check if the username and password are valid
        if userfound != None:
            passmatch=collection.find_one({"Password":password})
            if passmatch != None:
                #self.master.destroy()
                self.open_game_window(usr)
            else:
                self.error_label.config(text="Invalid password.")
        else:
            # If the login fails, display an error message
            self.error_label.config(text="Invalid username.")

    def open_game_window(self,user):
        #print("in opengame")
        #self.master.withdraw()  # Hide the main screen
        '''game_screen = tk.Toplevel(self)  # Create a new window
        game_page=Game2048(game_screen)  # Open the signup page
        game_page.mainloop()'''
        window=Game2048(self,user) #Open the game page
        window.mainloop()

# Create the login page object and run the main event loop
'''root = tk.Tk()
login_page = LoginPage(root)
root.mainloop()'''

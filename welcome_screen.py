import tkinter as tk
from register import *
from login import *
from PIL import Image, ImageTk

class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.master = master
        self.geometry("1920x1080")

        # create a frame to hold the login and signup buttons
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True)

        #Adding Image 
        self.img = Image.open("images/gameimage.png")
        self.resized_img= self.img.resize((300,300),Image.Resampling.LANCZOS)
        self.converted_img = ImageTk.PhotoImage(self.resized_img)
        self.label = tk.Label(self.frame, image= self.converted_img)
        self.label.grid(row=0,column=0,columnspan=2,padx=10, pady=10)

        # create welcome message label
        self.welcome_label = tk.Label(self.frame, text="Welcome to the Game!", font=("Arial", 24,"bold"), foreground="indian red2",bg ="white", highlightthickness=2, highlightbackground= "#cd5c5c",width=20, )
        self.welcome_label.grid(row=1,column=0,columnspan=2,padx=25,pady=25)

        # create the login button
        self.login_button = tk.Button(self.frame, text="Login", font=("Arial", 12,"bold"), width=12, height=2, bg="brown2",fg="white", activebackground="antique white2",command=self.open_login_page)
        self.login_button.grid(row=2, column=0, padx=10, pady=10)

        # create the signup button
        self.signup_button = tk.Button(self.frame, text="Signup", font=("Arial", 12,"bold"), width=12, height=2, bg="sienna2",fg="white" , activebackground="antique white2",command=self.open_signup_page)
        self.signup_button.grid(row=2, column=1, padx=10, pady=10)

        # center the buttons in the frame
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
    
    def open_login_page(self):
        #import login
        #self.master.withdraw()  # Hide the main screen
        #login_screen = tk.Toplevel(self)  # Create a new window
        LoginPage(self)  # Open the login page
        #login_page.mainloop()  # Start the login page loop
    
    def open_signup_page(self):
        #import register
        #self.master.withdraw()  # Hide the main screen
        #signup_screen = tk.Toplevel(self)  # Create a new window
        RegistrationForm(self)  # Open the signup page
        #signup_page.mainloop()  # Start the signup page loop

if __name__ == "__main__":
    #root = tk.Tk()
    main_screen = MainScreen()
    main_screen.mainloop()

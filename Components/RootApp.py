import re
import tkinter as tk
from tkinter import messagebox as mb

import Permissions
from Components import TablesChoice
from db_controller import Database


class Root:
    app = Database()
    perm = Permissions.Permission()

    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")
        self.root.grid_columnconfigure([0, 1], weight=1)
        self.root.geometry("350x200+550+280")

        self.lbl_connection_state = tk.Label(self.root, text="", font="Sans 14")
        self.lbl_connection_state.grid(row=0, columnspan=2)

        self.lbl_email = tk.Label(self.root, text="E-mail", font="Sans 14")
        self.lbl_password = tk.Label(self.root, text="Password", font="Sans 14")
        self.lbl_email.grid(row=1, column=0, padx=5)
        self.lbl_password.grid(row=2, column=0, padx=5)

        self.ent_email = tk.Entry(self.root, width=20)
        self.ent_password = tk.Entry(self.root, width=20)
        self.ent_email.grid(row=1, column=1)
        self.ent_password.grid(row=2, column=1)

        self.ent_email.focus_set()

        self.btn_submit_signUp = tk.Button(
            self.root, text="Sign up", command=self.register
        )
        self.btn_submit_signUp.grid(row=3, column=0, pady=12)

        self.btn_submit_signUIn = tk.Button(
            self.root, text="Sign in", command=self.authorization
        )
        self.btn_submit_signUIn.grid(row=3, column=1)

        self.lbl_error = tk.Label(self.root, text="", font="Sans 15", fg="red")
        self.lbl_error.grid(row=4, columnspan=2)

        self.check_value = tk.IntVar()
        self.btn_check = tk.Checkbutton(
            self.root,
            text="Get full access",
            variable=self.check_value,
            onvalue=1,
            offvalue=0,
        )
        self.btn_check.grid(row=5, column=0, padx=5)

        self.btn_exit = tk.Button(
            self.root, text="Exit", width=8, command=self.root.destroy
        )
        self.btn_exit.grid(row=5, column=1, padx=10)

        if self.app.connection:
            self.lbl_connection_state.configure(text="Connection success.", fg="green")
        else:
            self.lbl_connection_state.configure(text="Connection error.", fg="red")
            mb.showerror("Error", "Something went wrong. We cant connect to DataBase.")
            self.root.destroy()

    def validate_form(self):
        """Checking on valid user insert"""
        email_valid = False
        password_valid = False
        password = self.ent_password.get()
        email = self.ent_email.get()
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, email) and len(password) > 4:
            email_valid = True
            password_valid = True
        return email_valid, password_valid

    def register(self):
        """Register user"""
        email_valid, password_valid = self.validate_form()
        if email_valid and password_valid:
            self.perm.checkPermission(self.check_value.get())
            permission = self.perm.permission
            isExist = Root.app.get_user(self.ent_email.get())
            if not isExist:
                self.app.create_user(
                    self.ent_email.get(),
                    self.ent_password.get(),
                    permission,
                )
                self.lbl_error["text"] = ""
                self.app.permission = "ADMIN" if self.check_value.get() == 1 else "USER"
                print(f"[INFO] Success sign up as <{self.ent_email.get()}>.")

                self.queriesWindow = tk.Tk()
                self.queries = TablesChoice.Tables(self.queriesWindow)
                self.root.destroy()
            else:
                self.lbl_error["text"] = "Such user already exist."
                print("[INFO] Error while registration. Such user already exist.")
        else:
            self.lbl_error["text"] = "Invalid email/password"
            print("[INFO] Error while registration. Invalid email/password.")

    def authorization(self):
        """Authorize user"""
        response = self.app.get_user(self.ent_email.get())
        if response:
            email_response = list(response[0])[1]
            password_response = list(response[0])[2]
            permission_response = list(response[0])[3]
            if email_response and password_response == self.ent_password.get():
                self.lbl_error["text"] = ""
                self.perm.permission = permission_response

                self.queriesWindow = tk.Tk()
                self.queries = TablesChoice.Tables(self.queriesWindow)
                self.root.destroy()

                print(f"[INFO] Success sign in as <{email_response}>.")
            else:
                self.lbl_error["text"] = "Invalid email/password."
                print("[INFO] Error while authorization. Invalid email/password.")
        elif not response:
            self.lbl_error["text"] = "Invalid email/password."
            print("[INFO] Invalid email/password")

import re
import tkinter as tk
from tkinter import ttk

from Components import RootApp, TablesChoice
from Permissions import Permission


class ShowUsersTable:
    def __init__(self, root, order="id", isFind=False, findData=None):
        self.showUser_window = root
        self.showUser_window.title("DB content")
        self.showUser_window.geometry("1200x700+100+50")

        frame_table = tk.Frame(self.showUser_window)
        frame_top = tk.Frame(self.showUser_window, height=40)

        btn_add = tk.Button(frame_top, text="Add", width=8, pady=5, padx=6, command=self.addUser_window)
        btn_delete = tk.Button(frame_top, text="Delete", width=8, pady=5, padx=6, command=self.deleteUser_window)
        btn_sort = tk.Button(frame_top, text="Sort", width=8, pady=5, padx=6, command=self.sortUser_window)
        btn_find = tk.Button(frame_top, text="Find", width=8, pady=5, padx=6, command=self.findUser_window)
        btn_update = tk.Button(frame_top, text="Update", width=8, pady=5, padx=6, command=self.updateUser_window)
        btn_refresh = tk.Button(frame_top, text="Refresh", width=8, pady=5, padx=6, command=self.refreshUser_window)
        btn_exit = tk.Button(frame_top, text="Exit", width=8, pady=5, padx=6, command=self.exitUserTable)

        btn_add.pack(side=tk.LEFT)
        btn_delete.pack(side=tk.LEFT)
        btn_sort.pack(side=tk.LEFT)
        btn_find.pack(side=tk.LEFT)
        btn_update.pack(side=tk.LEFT)
        btn_refresh.pack(side=tk.LEFT)
        btn_exit.pack(side=tk.RIGHT)

        if isFind:
            self.record = findData
        elif not isFind:
            self.record = RootApp.Root.app.show("users", order)

        heads = ["id", "email", "password", "permission"]
        self.table = ttk.Treeview(frame_table, show="headings")
        self.table["columns"] = heads

        for header in heads:
            self.table.heading(header, text=header, anchor="center")
            self.table.column(header, anchor="center")
            self.table.column("id", width=15)
            self.table.column("email", width=25)
            self.table.column("password", width=25)
            self.table.column("permission", width=25)

        for row in self.record:
            self.table.insert("", "end", values=row)

        self.scroll_panel = ttk.Scrollbar(frame_table, command=self.table.yview)
        self.scroll_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=self.scroll_panel.set)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

        frame_top.pack(fill=tk.BOTH)
        frame_table.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.table.bind("<<TreeviewSelect>>", self.select)

        self.id_select = 0

    def select(self, event):
        for selection in self.table.selection():
            item = self.table.item(selection)
            self.id_select = item["values"][0]

    def exitUserTable(self):
        self.showUser_window.destroy()
        refreshTableChoice_window = tk.Tk()
        refreshTableChoice = TablesChoice.Tables(refreshTableChoice_window)

    def addUser_window(self):
        """Add user window"""
        self.addUser_window = tk.Tk()
        self.addUser_window.title("Add user row")
        self.addUser_window.geometry("350x150+500+250")
        self.addUser_window.grid_columnconfigure([0, 1], weight=1)

        self.lbl_addError = tk.Label(
            self.addUser_window, text="", fg="red", font="Sans 15"
        )
        self.lbl_addError.grid(row=0, columnspan=3)

        lbl_email = tk.Label(
            self.addUser_window, text="E-mail", font="Sans 13", padx=5, pady=5
        )
        lbl_password = tk.Label(
            self.addUser_window, text="Password", font="Sans 13", padx=5, pady=5
        )

        lbl_email.grid(row=1, column=0, sticky=tk.E)
        lbl_password.grid(row=2, column=0, sticky=tk.E)

        self.ent_email = tk.Entry(self.addUser_window, width=20)
        self.ent_password = tk.Entry(self.addUser_window, width=20)

        self.ent_email.grid(row=1, column=1)
        self.ent_password.grid(row=2, column=1)

        self.ent_email.focus_set()

        self.check_value = tk.IntVar()
        self.btn_check = tk.Checkbutton(self.addUser_window, text="Get full access", variable=self.check_value, onvalue=1, offvalue=0,)
        self.btn_check.grid(row=3, column=1)

        btn_submit_add = tk.Button(self.addUser_window, text="Add", width=8, command=self.create_new_UserRow)

        btn_submit_add.grid(row=4, columnspan=3)

        # Fixing doesn't working check_value
        self.empty = tk.Label(self.addUser_window, textvariable=self.check_value)

    def create_new_UserRow(self):
        """Create new user row in DB"""
        email = self.ent_email.get()
        password = self.ent_password.get()
        role = self.empty["text"]
        perm_check = Permission()
        perm_check.checkPermission(role)

        isExist = RootApp.Root.app.get_user(email)
        if not isExist:
            if (
                re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email)
                and len(password) > 4
            ):
                RootApp.Root.app.create_user(email, password, perm_check.permission)

                self.addUser_window.destroy()
                self.showUser_window.destroy()

                refresh_create_window = tk.Tk()
                refresh_create = ShowUsersTable(refresh_create_window)
                print("[INFO] Successfully added")
            else:
                self.lbl_addError["text"] = "Invalid email/password."
                print(
                    "[INFO] Error while adding in User table. Invalid email/password."
                )
        else:
            self.lbl_addError["text"] = "Such user is already exist."
            print("[INFO] Error while adding in User table. Such user is already exist")

    def deleteUser_window(self):
        """Delete user window"""
        if self.id_select:
            self.deleteUser_window = tk.Tk()
            self.deleteUser_window.title("Delete Book row")
            self.deleteUser_window.geometry("270x130+500+250")

            lbl_confirm = tk.Label(
                self.deleteUser_window, text="Are you sure?", font="Sans 21"
            )
            lbl_confirm.pack()

            btn_cancel = tk.Button(self.deleteUser_window, text="No", width=7, command=self.deleteUser_window.destroy,)
            btn_confirm = tk.Button(
                self.deleteUser_window, text="Yes", width=7, command=self.deleteUser_row
            )

            btn_cancel.pack(side=tk.LEFT)
            btn_confirm.pack(side=tk.RIGHT)
        else:
            self.error_noSelected()
            print("[INFO] Error while deleting. Element did not select.")

    def deleteUser_row(self):
        """Delete row from DataBase"""
        RootApp.Root.app.delete_by_ID(self.id_select, "users")
        self.deleteUser_window.destroy()
        self.showUser_window.destroy()

        refresh_deleteBook_window = tk.Tk()
        refresh_deleteBook = ShowUsersTable(refresh_deleteBook_window)

        print("[INFO] Successfully deleted.")

    def error_window(self):
        error_window = tk.Tk()
        error_window.title("Error")
        error_window.geometry("280x75+500+250")
        label = tk.Label(
            error_window, text="Something went wrong. Fill in only one field"
        )
        label.pack()
        button = tk.Button(
            error_window, text="Ok", width=10, command=error_window.destroy
        )
        button.pack(side=tk.RIGHT)
        error_window.mainloop()

    def sortUser_window(self):
        self.sortUser_window = tk.Toplevel(self.showUser_window)
        self.sortUser_window.title("Sorting data")
        self.sortUser_window.geometry("380x80+500+250")

        lbl_title = tk.Label(
            self.sortUser_window, text="Choose column you want to sort", font="Sans 15"
        )
        lbl_title.pack()

        btn_idColumn = tk.Button(
            self.sortUser_window, text="ID", command=lambda: self.sort_column("id")
        )
        btn_emailColumn = tk.Button(
            self.sortUser_window,
            text="E-mail",
            command=lambda: self.sort_column("email"),
        )
        btn_passwordColumn = tk.Button(
            self.sortUser_window,
            text="Password",
            command=lambda: self.sort_column("password"),
        )
        btn_permissionColumn = tk.Button(
            self.sortUser_window,
            text="Permission",
            command=lambda: self.sort_column("permission"),
        )

        btn_idColumn.pack(side=tk.LEFT, padx=4)
        btn_emailColumn.pack(side=tk.LEFT, padx=4)
        btn_passwordColumn.pack(side=tk.LEFT, padx=4)
        btn_permissionColumn.pack(side=tk.LEFT, padx=4)

    def sort_column(self, column):
        self.sortUser_window.destroy()
        self.showUser_window.destroy()

        refresh_sortColumn_window = tk.Tk()
        refresh_sortColumn = ShowUsersTable(refresh_sortColumn_window, column)

        print("[INFO] Successfully sorted.")

    def findUser_window(self):
        self.findUser_window = tk.Toplevel(self.showUser_window)
        self.findUser_window.title("Find in DB")
        self.findUser_window.geometry("380x140+500+250")

        lbl_combobox_title = tk.Label(
            self.findUser_window, text="Choose column you want to find", font="Sans 21"
        )
        self.lbl_findError = tk.Label(
            self.findUser_window, text="", font="Sans 15", fg="red"
        )
        lbl_combobox_title.pack()
        self.lbl_findError.pack()

        self.columns = ["email", "password", "permission"]
        self.selected_column = tk.StringVar()
        self.cmb_find = ttk.Combobox(
            self.findUser_window, textvariable=self.selected_column, width=12
        )
        self.cmb_find["values"] = self.columns
        self.cmb_find["state"] = "readonly"

        self.cmb_find.pack(side=tk.LEFT, padx=7)

        self.cmb_find.bind("<<ComboboxSelected>>", self.columnSearch_changed)

        self.ent_search = tk.Entry(self.findUser_window, width=15)
        self.ent_search.pack(side=tk.LEFT)

        btn_search = tk.Button(
            self.findUser_window, text="Search", command=self.search_rows
        )
        btn_search.pack(side=tk.LEFT)

        self.choice_find = None

    def columnSearch_changed(self, event):
        self.choice_find = self.cmb_find.get()

    def search_rows(self):
        if self.choice_find != None:
            self.isValid = False
            self.validate_column(self.choice_find)
            response = RootApp.Root.app.search_element(
                "users", self.choice_find, self.ent_search.get()
            )
            if self.isValid and response:
                self.findUser_window.destroy()
                self.showUser_window.destroy()

                refresh_searchRows_window = tk.Tk()
                refresh_searchRows = ShowUsersTable(
                    refresh_searchRows_window, isFind=True, findData=response
                )

                print("[INFO] Successfully founded.")
            elif self.isValid and not response:
                self.lbl_findError["text"] = "Nothing was founded."
                print("[INFO] Error while founding. Nothing was founded.")
            elif not self.isValid:
                self.lbl_findError["text"] = "Incorrect input value for search."
                print("[INFO] Error while founding. Incorrect input.")
        else:
            self.lbl_findError["text"] = "No search field selected."
            print("[INFO] No search field selected.")

    def validate_add(self, email="none", password="none", permission="none"):
        self.valid_email = False
        self.valid_password = False
        self.valid_permission = False

        if re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email):
            self.valid_email = True

        if len(password) > 4:
            self.valid_password = True

        if permission.isalpha():
            self.valid_permission = True

    def validate_column(self, choice, command="search"):
        if choice == "email":
            self.validate_add(
                email=self.ent_search.get()
                if command == "search"
                else self.ent_update.get()
            )
            self.isValid = self.valid_email
        if choice == "password":
            self.validate_add(
                password=self.ent_search.get()
                if command == "search"
                else self.ent_update.get()
            )
            self.isValid = self.valid_password
        if choice == "permission":
            self.validate_add(
                permission=self.ent_search.get()
                if command == "search"
                else self.ent_update.get()
            )
            self.isValid = self.valid_permission

    def refreshUser_window(self):
        self.showUser_window.destroy()
        refreshUser_window = tk.Tk()
        refreshUser = ShowUsersTable(refreshUser_window)

        print("[INFO] Successfully refreshed.")

    def updateUser_window(self):
        if self.id_select != 0:
            self.updateUser_window = tk.Tk()
            self.updateUser_window.title("Update row")
            self.updateUser_window.geometry("380x140+500+250")

            lbl_updateUser = tk.Label(
                self.updateUser_window,
                text="Choose field for updating.",
                font="Sans 21",
            )
            self.lbl_error_updateUser = tk.Label(
                self.updateUser_window, text="", fg="red", font="Sans 16"
            )
            lbl_updateUser.pack()
            self.lbl_error_updateUser.pack()

            self.update_columns = ["email", "password", "permission"]
            self.update_selected_column = tk.StringVar()
            self.cmb_update = ttk.Combobox(
                self.updateUser_window,
                textvariable=self.update_selected_column,
                width=12,
            )
            self.cmb_update["values"] = self.update_columns
            self.cmb_update["state"] = "readonly"

            self.cmb_update.pack(side=tk.LEFT, padx=7)

            self.cmb_update.bind("<<ComboboxSelected>>", self.columnUpdate_changed)

            self.ent_update = tk.Entry(self.updateUser_window, width=15)
            self.ent_update.pack(side=tk.LEFT)

            btn_update = tk.Button(
                self.updateUser_window, text="Update", command=self.update_user
            )
            btn_update.pack(side=tk.LEFT)
            self.choice_update = None

        elif self.id_select == 0:
            self.error_noSelected()
            print("[INFO] Nothing was selected.")

    def columnUpdate_changed(self, event):
        self.choice_update = self.cmb_update.get()

    def error_noSelected(self):
        error_noSelected = tk.Tk()
        error_noSelected.title("Error")
        error_noSelected.geometry("400x110+500+250")

        lbl_error_noSelect = tk.Label(
            error_noSelected,
            text="Nothing was select.\nSelect row you want to update.",
            fg="red",
            font="Sans 18",
        )
        lbl_error_noSelect.pack()

        btn_close_noSelect_window = tk.Button(
            error_noSelected, text="Ok", width=7, command=error_noSelected.destroy
        )
        btn_close_noSelect_window.pack(side=tk.RIGHT)

        error_noSelected.mainloop()

    def update_user(self):
        if self.choice_update != None:
            self.validate_column(self.choice_update, "update")
            if self.isValid:
                RootApp.Root.app.update_element(
                    "users", self.choice_update, self.ent_update.get(), self.id_select
                )
                self.updateUser_window.destroy()
                self.showUser_window.destroy()
                refresh_updateUser_window = tk.Tk()
                refresh_updateUser = ShowUsersTable(refresh_updateUser_window)
                print("[INFO] Successfully updated.")
            else:
                self.lbl_error_updateUser["text"] = "Invalid input value."
                print("[INFO] Error while updating. Invalid input value")
        else:
            self.lbl_error_updateUser["text"] = "No search field selected."
            print("[INFO] No search field selected.")

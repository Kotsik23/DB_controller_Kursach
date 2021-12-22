import tkinter as tk

from Components import BooksTable, RootApp, UsersTable


class Tables:
    def __init__(self, root):
        self.db_tables = root
        self.db_tables.geometry("300x150+550+280")
        self.db_tables.title("DB management")
        self.db_tables.grid_columnconfigure([0, 1, 2, 3], weight=1)

        lbl_title = tk.Label(
            self.db_tables, text="DB tables", font=("Sans", 20), padx=10
        )
        lbl_title.grid(row=0, columnspan=2)

        self.lbl_permission_state = tk.Label(self.db_tables, text="", font="Sans 14")
        self.lbl_permission_state.grid(row=1, columnspan=2)

        btn_books_table = tk.Button(
            self.db_tables, text="Books", width=7, command=self.show_books_table
        )
        btn_users_table = tk.Button(
            self.db_tables, text="Users", width=7, command=self.show_users_table
        )

        btn_books_table.grid(row=2, column=0, padx=20)
        btn_users_table.grid(row=2, column=1, padx=20)

        btn_back = tk.Button(self.db_tables, text="Back", command=self.back_root)

        btn_back.grid(row=3, column=0, pady=20)

    def back_root(self):
        """Back to the root window"""
        self.db_tables.destroy()
        rootWindow = tk.Tk()
        root = RootApp.Root(rootWindow)

    def show_books_table(self):
        """Show content of books table"""
        self.db_tables.destroy()
        self.show_window = tk.Tk()
        self.show = BooksTable.ShowBooksTable(self.show_window)
        print("[INFO] Successfully showed.")

    def show_users_table(self):
        """Show content of users table"""
        if RootApp.Root.perm.permission == "ADMIN":
            self.db_tables.destroy()
            self.show_window = tk.Tk()
            self.show = UsersTable.ShowUsersTable(self.show_window)
            print("[INFO] Successfully showed.")
        elif RootApp.Root.perm.permission == "USER":
            self.lbl_permission_state.configure(
                text="Access denied. Not enough permissions.", fg="red"
            )
            print("[INFO] Not enough permissions.")

import tkinter as tk
from tkinter import ttk

from Components import RootApp, TablesChoice


class ShowBooksTable:
    def __init__(self, root, order="id", isFind=False, findData=None):
        self.showBook_window = root
        self.showBook_window.title("DB content")
        self.showBook_window.geometry("1200x700+100+50")

        frame_table = tk.Frame(self.showBook_window)
        frame_top = tk.Frame(self.showBook_window, height=40)

        btn_add = tk.Button(frame_top, text='Add', width=8, pady=5, padx=6, command=self.addBook_window)
        btn_delete = tk.Button(frame_top, text='Delete', width=8, pady=5, padx=6, command=self.deleteBook_window)
        btn_sort = tk.Button(frame_top, text='Sort', width=8, pady=5, padx=6, command=self.sortBook_window)
        btn_find = tk.Button(frame_top, text="Find", width=8, pady=5, padx=6, command=self.findBook_window)
        btn_update = tk.Button(frame_top, text="Update", width=8, pady=5, padx=6, command=self.updateBook_window)
        btn_refresh = tk.Button(frame_top, text="Refresh", width=8, pady=5, padx=6, command=self.refreshBook_window)
        btn_moreInfo = tk.Button(frame_top, text="Author Info", width=8, pady=5, padx=6, command=self.author_info)
        btn_exit = tk.Button(frame_top, text='Exit', width=8, pady=5, padx=6, command=self.exitBookTable)

        btn_add.pack(side=tk.LEFT)
        btn_delete.pack(side=tk.LEFT)
        btn_sort.pack(side=tk.LEFT)
        btn_find.pack(side=tk.LEFT)
        btn_update.pack(side=tk.LEFT)
        btn_refresh.pack(side=tk.LEFT)
        btn_moreInfo.pack(side=tk.LEFT)
        btn_exit.pack(side=tk.RIGHT)

        if isFind:  # Display founded data
            self.record = findData
        elif not isFind:  # Display all data of DB
            self.record = RootApp.Root.app.show("books", order)

        heads = ['id', 'name', 'author', 'user rating', 'reviews', 'price', 'year', 'genre']
        self.table = ttk.Treeview(frame_table, show="headings")
        self.table['columns'] = heads

        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')
            self.table.column("id", width=35)
            self.table.column("name", width=450, anchor=tk.W)
            self.table.column("author", anchor=tk.W)
            self.table.column("user rating", width=70)
            self.table.column("reviews", width=130)
            self.table.column("price", width=70)
            self.table.column("year", width=100)
            self.table.column("genre", width=120, anchor=tk.W)

        for row in self.record:
            self.table.insert('', 'end', values=row)

        self.scroll_panel = ttk.Scrollbar(frame_table, command=self.table.yview)
        self.scroll_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=self.scroll_panel.set)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

        frame_top.pack(fill=tk.BOTH)
        frame_table.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.table.bind("<<TreeviewSelect>>", self.select)
        self.table.bind("<Double-Button-1>", self.doubleClick_authorInfo)
        self.showBook_window.bind("<Command-a>", self.bind_add)
        self.showBook_window.bind("<Command-d>", self.bind_delete)
        self.showBook_window.bind("<Command-s>", self.bind_sort)
        self.showBook_window.bind("<Command-f>", self.bind_find)
        self.showBook_window.bind("<Command-u>", self.bind_update)
        self.showBook_window.bind("<Command-r>", self.bind_refresh)
        self.showBook_window.bind("<Command-i>", self.bind_info)
        self.showBook_window.bind("<Command-e>", self.bind_exit)
        self.id_select = 0

    def select(self, event):
        """Getting data when selecting a row"""
        for selection in self.table.selection():
            item = self.table.item(selection)
            self.id_select = item["values"][0]
            self.author_select = item["values"][2]

    def doubleClick_authorInfo(self, event):
        self.author_info()

    def exitBookTable(self):
        self.showBook_window.destroy()
        refreshTableChoice_window = tk.Tk()
        refreshTableChoice = TablesChoice.Tables(refreshTableChoice_window)

    def addBook_window(self):
        """Add book window"""
        addBook_window = tk.Tk()
        addBook_window.title("Add Book row")
        addBook_window.geometry("480x250+500+250")
        addBook_window.grid_columnconfigure([1, 2], weight=1)

        lbl_name = tk.Label(addBook_window, text="Name", font="Sans 13", padx=5, pady=5)
        lbl_author = tk.Label(addBook_window, text="Author", font="Sans 13", padx=5, pady=5)
        lbl_user_rating = tk.Label(addBook_window, text="User rating", font="Sans 13", padx=5, pady=5)
        lbl_reviews = tk.Label(addBook_window, text="Reviews", font="Sans 13", padx=5, pady=5)
        lbl_price = tk.Label(addBook_window, text="Price", font="Sans 13", padx=5, pady=5)
        lbl_year = tk.Label(addBook_window, text="Year", font="Sans 13", padx=5, pady=5)
        lbl_genre = tk.Label(addBook_window, text="Genre", font="Sans 13", padx=5, pady=5)

        lbl_name.grid(row=0, column=0, sticky=tk.E)
        lbl_author.grid(row=1, column=0, sticky=tk.E)
        lbl_user_rating.grid(row=2, column=0, sticky=tk.E)
        lbl_reviews.grid(row=3, column=0, sticky=tk.E)
        lbl_price.grid(row=4, column=0, sticky=tk.E)
        lbl_year.grid(row=5, column=0, sticky=tk.E)
        lbl_genre.grid(row=6, column=0, sticky=tk.E)

        self.lbl_nameError = tk.Label(addBook_window, text="", fg="red")
        self.lbl_authorError = tk.Label(addBook_window, text="", fg="red")
        self.lbl_user_ratingError = tk.Label(addBook_window, text="", fg="red")
        self.lbl_reviewsError = tk.Label(addBook_window, text="", fg="red")
        self.lbl_priceError = tk.Label(addBook_window, text="", fg="red")
        self.lbl_yearError = tk.Label(addBook_window, text="", fg="red")
        self.lbl_genreError = tk.Label(addBook_window, text="", fg="red")

        self.ent_name = tk.Entry(addBook_window, width=20)
        self.ent_author = tk.Entry(addBook_window, width=20)
        self.ent_user_rating = tk.Entry(addBook_window, width=20)
        self.ent_reviews = tk.Entry(addBook_window, width=20)
        self.ent_price = tk.Entry(addBook_window, width=20)
        self.ent_year = tk.Entry(addBook_window, width=20)
        self.ent_genre = tk.Entry(addBook_window, width=20)

        self.ent_name.grid(row=0, column=1)
        self.ent_author.grid(row=1, column=1)
        self.ent_user_rating.grid(row=2, column=1)
        self.ent_reviews.grid(row=3, column=1)
        self.ent_price.grid(row=4, column=1)
        self.ent_year.grid(row=5, column=1)
        self.ent_genre.grid(row=6, column=1)

        self.ent_name.focus_set()

        btn_submit_add = tk.Button(addBook_window, text="Add", width=8, command=lambda: self.create_new_BooksRow(addBook_window))

        btn_submit_add.grid(row=7, columnspan=3)

    def create_new_BooksRow(self, addBook_window):
        """Create new book row in DB"""
        name = self.ent_name.get()
        author = self.ent_author.get()
        user_rating = self.ent_user_rating.get()
        reviews = self.ent_reviews.get()
        price = self.ent_price.get()
        year = self.ent_year.get()
        genre = self.ent_genre.get()

        self.validate_add(name, author, user_rating, reviews, price, year, genre)

        if self.valid_name and self.valid_author and self.valid_user_rating and self.valid_reviews \
                and self.valid_price and self.valid_year and self.valid_genre:
            RootApp.Root.app.addBook_row(name, author, user_rating, reviews, price, year, genre)
            addBook_window.destroy()
            self.showBook_window.destroy()

            self.refresh_create_window = tk.Tk()
            self.refresh_create = ShowBooksTable(self.refresh_create_window)

            print('[INFO] Successfully added')
        else:
            print('[INFO] Error while adding. Invalid input.')
            self.error_addInput()

    def error_addInput(self):
        """A window with an input error when adding new row"""
        if not self.valid_name:
            self.lbl_nameError["text"] = "NAME field is incorrect."
            self.lbl_nameError.grid(row=0, column=3, sticky=tk.W)
        else:
            self.lbl_nameError["text"] = ""
            self.lbl_nameError.grid(row=0, column=3, sticky=tk.W)

        if not self.valid_author:
            self.lbl_authorError["text"] = "AUTHOR field is incorrect."
            self.lbl_authorError.grid(row=1, column=3, sticky=tk.W)
        else:
            self.lbl_authorError["text"] = ""
            self.lbl_authorError.grid(row=1, column=3, sticky=tk.W)

        if not self.valid_user_rating:
            self.lbl_user_ratingError["text"] = "USER rating field is incorrect."
            self.lbl_user_ratingError.grid(row=2, column=3, sticky=tk.W)
        else:
            self.lbl_user_ratingError["text"] = ""
            self.lbl_user_ratingError.grid(row=2, column=3, sticky=tk.W)

        if not self.valid_reviews:
            self.lbl_reviewsError["text"] = "REVIEWS field is incorrect."
            self.lbl_reviewsError.grid(row=3, column=3, sticky=tk.W)
        else:
            self.lbl_reviewsError["text"] = ""
            self.lbl_reviewsError.grid(row=3, column=3, sticky=tk.W)

        if not self.valid_price:
            self.lbl_priceError["text"] = "PRICE field is incorrect."
            self.lbl_priceError.grid(row=4, column=3, sticky=tk.W)
        else:
            self.lbl_priceError["text"] = ""
            self.lbl_priceError.grid(row=4, column=3, sticky=tk.W)

        if not self.valid_year:
            self.lbl_yearError["text"] = "YEAR field is incorrect."
            self.lbl_yearError.grid(row=5, column=3, sticky=tk.W)
        else:
            self.lbl_yearError["text"] = ""
            self.lbl_yearError.grid(row=5, column=3, sticky=tk.W)

        if not self.valid_genre:
            self.lbl_genreError["text"] = "GENRE field is incorrect."
            self.lbl_genreError.grid(row=6, column=3, sticky=tk.W)
        else:
            self.lbl_genreError["text"] = ""
            self.lbl_genreError.grid(row=6, column=3, sticky=tk.W)

    def validate_add(self, name="none", author="none", user_rating="0.0", reviews="0", price="0", year="0", genre="none"):
        """validation of fields before adding a new row"""
        self.valid_name = False
        self.valid_author = False
        self.valid_user_rating = False
        self.valid_reviews = False
        self.valid_price = False
        self.valid_year = False
        self.valid_genre = False

        if 2 < len(name) < 200:
            self.valid_name = True

        if 0 < len(author) < 150:
            self.valid_author = True

        if len(user_rating) == 3 and user_rating.find(".") != -1 and user_rating[0].isdigit() and user_rating[2].isdigit():
            self.valid_user_rating = True

        if 0 < len(reviews) < 1e6 and reviews.isdigit():
            self.valid_reviews = True

        if 0 < len(price) < 10 and price.isdigit():
            self.valid_price = True

        if len(year) == 4 and year.isdigit():
            self.valid_year = True

        if 3 < len(genre) < 100:
            self.valid_genre = True

    def deleteBook_window(self):
        """Delete book window"""
        if self.id_select:
            deleteBook_window = tk.Tk()
            deleteBook_window.title("Delete Book row")
            deleteBook_window.geometry("270x130+500+250")

            lbl_confirm = tk.Label(deleteBook_window, text="Are you sure?", font="Sans 21")
            lbl_confirm.pack()

            btn_cancel = tk.Button(deleteBook_window, text="No", width=7, command=deleteBook_window.destroy)
            btn_confirm = tk.Button(deleteBook_window, text="Yes", width=7, command=lambda: self.deleteBook_row(deleteBook_window))

            btn_cancel.pack(side=tk.LEFT)
            btn_confirm.pack(side=tk.RIGHT)
        else:
            self.error_noSelected()
            print('[INFO] Error while deleting. Element did not select.')

    def deleteBook_row(self, deleteBook_window):
        """Delete book row from DataBase"""
        RootApp.Root.app.delete_by_ID(self.id_select, "books")
        deleteBook_window.destroy()
        self.showBook_window.destroy()

        refresh_deleteBook_window = tk.Tk()
        refresh_deleteBook = ShowBooksTable(refresh_deleteBook_window)

        print('[INFO] Successfully deleted.')

    def sortBook_window(self):
        """Sorting window for the selected column"""
        sortBook_window = tk.Toplevel(self.showBook_window)
        sortBook_window.title("Sorting data")
        sortBook_window.geometry("680x80+330+250")

        lbl_title = tk.Label(sortBook_window, text="Choose column you want to sort", font="Sans 15")
        lbl_title.pack()

        btn_idColumn = tk.Button(sortBook_window, text="ID", command=lambda: self.sort_column("id", sortBook_window))
        btn_nameColumn = tk.Button(sortBook_window, text="Name", command=lambda: self.sort_column("name", sortBook_window))
        btn_authorColumn = tk.Button(sortBook_window, text="Author", command=lambda: self.sort_column("author", sortBook_window))
        btn_user_ratingColumn = tk.Button(sortBook_window, text="User rating", command=lambda: self.sort_column("user_rating", sortBook_window))
        btn_reviewsColumn = tk.Button(sortBook_window, text="Reviews", command=lambda: self.sort_column("reviews", sortBook_window))
        btn_priceColumn = tk.Button(sortBook_window, text="Price", command=lambda: self.sort_column("price", sortBook_window))
        btn_yearColumn = tk.Button(sortBook_window, text="Year", command=lambda: self.sort_column("year", sortBook_window))
        btn_genreColumn = tk.Button(sortBook_window, text="Genre", command=lambda: self.sort_column("genre", sortBook_window))

        btn_idColumn.pack(side=tk.LEFT, padx=4)
        btn_nameColumn.pack(side=tk.LEFT, padx=4)
        btn_authorColumn.pack(side=tk.LEFT, padx=4)
        btn_user_ratingColumn.pack(side=tk.LEFT, padx=4)
        btn_reviewsColumn.pack(side=tk.LEFT, padx=4)
        btn_priceColumn.pack(side=tk.LEFT, padx=4)
        btn_yearColumn.pack(side=tk.LEFT, padx=4)
        btn_genreColumn.pack(side=tk.LEFT, padx=4)

    def sort_column(self, column, sortBook_window):
        """Sorting rows of DataBase"""
        sortBook_window.destroy()
        self.showBook_window.destroy()

        refresh_sortColumn_window = tk.Tk()
        refresh_sortColumn = ShowBooksTable(refresh_sortColumn_window, column)

        print("[INFO] Successfully sorted.")

    def findBook_window(self):
        """The record search window for the selected field"""
        findBook_window = tk.Tk()
        findBook_window.title("Find in DB")
        findBook_window.geometry("380x140+500+250")

        self.choice_find = None

        lbl_combobox_title = tk.Label(findBook_window, text="Choose column you want to find", font="Sans 21")
        self.lbl_findError = tk.Label(findBook_window, text="", font="Sans 15", fg="red")
        lbl_combobox_title.pack()
        self.lbl_findError.pack()

        self.fromTo_value = tk.StringVar()
        from_rdbtn = tk.Radiobutton(findBook_window, text="<", variable=self.fromTo_value, value=1)
        to_rdbtn = tk.Radiobutton(findBook_window, text=">", variable=self.fromTo_value, value=2)

        from_rdbtn.pack()
        to_rdbtn.pack()

        self.lbl_fromTo_value = tk.Label(findBook_window, textvariable=self.fromTo_value)

        self.columns = ["name", "author", "user_rating", "reviews", "price", "year", "genre"]
        self.selected_column = tk.StringVar()
        self.cmb_find = ttk.Combobox(findBook_window, textvariable=self.selected_column, width=12)
        self.cmb_find["values"] = self.columns
        self.cmb_find["state"] = "readonly"

        self.cmb_find.pack(side=tk.LEFT, padx=7)

        self.cmb_find.bind("<<ComboboxSelected>>", self.columnSearch_changed)

        self.ent_search = tk.Entry(findBook_window, width=15)
        self.ent_search.pack(side=tk.LEFT)

        btn_search = tk.Button(findBook_window, text="Search", command=lambda: self.search_rows(findBook_window))
        btn_search.pack(side=tk.LEFT)

    def columnSearch_changed(self, event):
        """Getting a value from the Combobox"""
        self.choice_find = self.cmb_find.get()

    def search_rows(self, findBook_window):
        """Search for a record by the selected parameters"""
        if self.choice_find != None:
            self.isValid = False
            self.validate_column(self.choice_find)
            sign = "<" if self.lbl_fromTo_value["text"] == 1 else ">"
            response = RootApp.Root.app.search_element("books", self.choice_find, self.ent_search.get(), sign)
            if self.isValid and response:
                findBook_window.destroy()
                self.showBook_window.destroy()

                refresh_searchRows_window = tk.Tk()
                refresh_searchRows = ShowBooksTable(refresh_searchRows_window, isFind=True, findData=response)
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

    def validate_column(self, choice, command="search"):
        """Validation of the selected field"""
        if choice == "name":
            self.validate_add(name=self.ent_search.get() if command == "search" else self.ent_update.get())
            self.isValid = self.valid_name
        elif choice == "author":
            self.validate_add(author=self.ent_search.get() if command == "search" else self.ent_update.get())
            self.isValid = self.valid_author
        elif choice == "user_rating":
            self.validate_add(user_rating=self.ent_search.get() if command == "search" else self.ent_update.get())
            self.isValid = self.valid_user_rating
        elif choice == "reviews":
            self.validate_add(reviews=self.ent_search.get() if command == "search" else self.ent_update.get())
            self.isValid = self.valid_reviews
        elif choice == "price":
            self.validate_add(price=self.ent_search.get() if command == "search" else self.ent_update.get())
            self.isValid = self.valid_price
        elif choice == "year":
            self.validate_add(year=self.ent_search.get() if command == "search" else self.ent_update.get())
            self.isValid = self.valid_year
        elif choice == "genre":
            self.validate_add(genre=self.ent_search.get() if command == "search" else self.ent_update.get())
            self.isValid = self.valid_genre

    def refreshBook_window(self):
        """Updating window contents"""
        self.showBook_window.destroy()
        refreshBook_window = tk.Tk()
        refreshBook = ShowBooksTable(refreshBook_window)

        print("[INFO] Successfully refreshed.")

    def updateBook_window(self):
        """Window for updating a specific record"""
        if self.id_select != 0:
            updateBook_window = tk.Tk()
            updateBook_window.title("Update row")
            updateBook_window.geometry("380x140+500+250")

            lbl_updateBook = tk.Label(updateBook_window, text="Choose field for updating.", font="Sans 21")
            self.lbl_error_updateBook = tk.Label(updateBook_window, text="", fg="red", font="Sans 16")
            lbl_updateBook.pack()
            self.lbl_error_updateBook.pack()

            self.update_columns = ["name", "author", "user_rating", "reviews", "price", "year", "genre"]
            self.update_selected_column = tk.StringVar()
            self.cmb_update = ttk.Combobox(updateBook_window, textvariable=self.update_selected_column, width=12)
            self.cmb_update["values"] = self.update_columns
            self.cmb_update["state"] = "readonly"

            self.cmb_update.pack(side=tk.LEFT, padx=7)

            self.cmb_update.bind("<<ComboboxSelected>>", self.columnUpdate_changed)

            self.ent_update = tk.Entry(updateBook_window, width=15)
            self.ent_update.pack(side=tk.LEFT)

            btn_update = tk.Button(updateBook_window, text="Update", command=lambda: self.update_book(updateBook_window))
            btn_update.pack(side=tk.LEFT)

            self.choice_update = None

        elif self.id_select == 0:
            self.error_noSelected()
            print("[INFO] Nothing was selected.")

    def columnUpdate_changed(self, event):
        """Getting a value from the Combobox"""
        self.choice_update = self.cmb_update.get()

    def error_noSelected(self):
        """Error window when there is no choice"""
        error_noSelected = tk.Tk()
        error_noSelected.title("Error")
        error_noSelected.geometry("400x110+500+250")

        lbl_error_noSelect = tk.Label(error_noSelected, text="Nothing was select.\nSelect row you want to manipulate.",
                                      fg="red", font="Sans 18")
        lbl_error_noSelect.pack()

        btn_close_noSelect_window = tk.Button(error_noSelected, text="Ok", width=7, command=error_noSelected.destroy)
        btn_close_noSelect_window.pack(side=tk.RIGHT)

        error_noSelected.mainloop()

    def update_book(self, updateBook_window):
        """Updating the contents of the selected field"""
        if self.choice_update != None:
            self.validate_column(self.choice_update, "update")
            if self.isValid:
                RootApp.Root.app.update_element("books", self.choice_update, self.ent_update.get(), self.id_select)
                updateBook_window.destroy()
                self.showBook_window.destroy()
                refresh_updateBook_window = tk.Tk()
                refresh_updateBook = ShowBooksTable(refresh_updateBook_window)
                print('[INFO] Successfully updated.')
            else:
                self.lbl_error_updateBook["text"] = "Invalid input value."
                print('[INFO] Error while updating. Invalid input value')
        else:
            self.lbl_error_updateBook["text"] = "No search field selected."
            print("[INFO] No search field selected.")

    def author_info(self):
        if self.id_select != 0:
            author_name = self.author_select
            data = RootApp.Root.app.search_author(author_name)
            if data:
                authorInfo_window = tk.Tk()
                authorInfo_window.title("Author Info")
                authorInfo_window.geometry("640x420+450+250")

                birth_year = data[0][2]
                death_year = data[0][3]
                country = data[0][4]
                description = data[0][5]

                lbl_authorName = tk.Label(authorInfo_window, text=author_name, font=("Ubuntu Mono", 32))
                lbl_authorName.pack()

                lbl_birthYear = tk.Label(authorInfo_window, text=f"Родился в {birth_year} году.", font=("Ubuntu Mono", 16))
                lbl_deathYear = tk.Label(authorInfo_window, text=f"Умер в {death_year} году.", font=("Ubuntu Mono", 16))
                lbl_country = tk.Label(authorInfo_window, text=f"Страна: {country}", font=("Ubuntu Mono", 16))
                lbl_birthYear.pack()
                lbl_deathYear.pack()
                lbl_country.pack()

                lbl_info = tk.Label(authorInfo_window, text="Краткие сведения", font=("Ubuntu Mono", 19))
                lbl_info.pack(pady=4)

                frm_description = tk.Frame(authorInfo_window)
                frm_description.pack()

                text = tk.Text(frm_description, width=65, height=12, wrap="word", highlightthickness=0,
                               font=("Ubuntu Mono", 16))
                text.insert('end', description)
                text.pack(pady=15)
                text["state"] = "disabled"
                # text["background"] = "#333232"  # For DARK Mac OS theme
                text["background"] = "#ececec"  # For LIGHT Mac OS theme

                btn_close = tk.Button(authorInfo_window, height=2, text="So interesting", font=("Ubuntu Mono", 15),
                                      command=authorInfo_window.destroy)
                btn_close.pack()
                authorInfo_window.mainloop()
                print('[INFO] Author info successfully showed.')
            else:
                self.noAuthor_errorWindow()
                print('[INFO] Error while showing info. No info about this author.')

        elif self.id_select == 0:
            self.error_noSelected()
            print("[INFO] Nothing was selected.")

    def noAuthor_errorWindow(self):
        noAuthor_errorWindow = tk.Tk()
        noAuthor_errorWindow.title("Error")
        noAuthor_errorWindow.geometry("410x90+500+250")

        error_msg = tk.Label(noAuthor_errorWindow, text="Nothing was founded about this author...", fg="red",
                             font="Sans 22")
        error_msg.pack()

        btn_close = tk.Button(noAuthor_errorWindow, text="Ok", command=noAuthor_errorWindow.destroy)
        btn_close.pack()

        noAuthor_errorWindow.mainloop()

    def bind_add(self, event):
        self.addBook_window()

    def bind_delete(self, event):
        self.deleteBook_window()

    def bind_sort(self, event):
        self.sortBook_window()

    def bind_find(self, event):
        self.findBook_window()

    def bind_update(self, event):
        self.updateBook_window()

    def bind_refresh(self, event):
        self.refreshBook_window()

    def bind_info(self, event):
        self.author_info()

    def bind_exit(self, event):
        self.exitBookTable()
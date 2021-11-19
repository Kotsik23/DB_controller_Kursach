import psycopg2
import psycopg2.extensions

from config import USER, PASSWORD, HOST, DB_NAME, USER_TABLE, BOOKS_TABLE, AUTHOR_TABLE


class Database:
    connection: psycopg2.extensions.connection

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DB_NAME,
            )
            self.connection.autocommit = True
            print("[INFO] Success connection while working withPostgre SQL")
        except psycopg2.Error as err:
            self.connection = None
            print("[INFO] Error while working withPostgre SQL", err)

    def create_user(self, email, password, permission):
        """Creating new user row in DataBase"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {USER_TABLE} (email, password, permission) VALUES (%s, %s, %s)",
                    (email, password, permission),
                )
                print("[INFO] Successfully created")
        except psycopg2.Error as err:
            print("[INFO] Error while creating new user", err)

    def get_user(self, email):
        """Getting data of user in DataBase"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {USER_TABLE} WHERE email='{email}'")
                email_response = cursor.fetchall()
                return email_response
        except psycopg2.Error as err:
            print("[INFO] Error while getting user", err)

    def show(self, table_choice, order):
        """Getting data of all rows of the table of DataBase"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_choice} ORDER BY {order}")
                response = cursor.fetchall()
                return response
        except psycopg2.Error as err:
            print("[INFO] Error while showing", err)

    def addBook_row(self, name, author, user_rating, reviews, price, year, genre):
        """Creating new book row in DataBase"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {BOOKS_TABLE} (name, author, user_rating, reviews, price, year, genre) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, author, user_rating, reviews, price, year, genre),
                )
        except psycopg2.Error as err:
            print("[INFO] Error while adding row", err)

    def delete_by_ID(self, id, table):
        """Delete row from DataBase by id"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {table} WHERE id={id}")
        except psycopg2.Error as err:
            print("[INFO] Error while deleting user", err)

    def search_element(self, table, column, value):
        """Search rows with specific parameters"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table} WHERE {column}='{value}'")
                response = cursor.fetchall()
                return response
        except psycopg2.Error as err:
            print("[INFO] Error while searching element.", err)

    def update_element(self, table, column, value, id):
        """Update exact column of the element"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE {table} SET {column} = '{value}' WHERE id = {id}")
        except psycopg2.Error as err:
            print("[INFO] Error while updating element", err)

    def search_author(self, author):
        """Search authors biography"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {AUTHOR_TABLE} where name='{author}'")
                response = cursor.fetchall()
                return response
        except psycopg2.Error as err:
            print("[INFO] Error while searching authors biography.", err)

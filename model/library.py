import csv
import os
from datetime import date, timedelta

from model.action_outcomes import LoginOutcome, AddBookOutcome, LoanOutcome, ReserveOutcome, RemoveBookOutcome, \
    RemoveLoanOutcome, AddUserOutcome
from model.book import Book
from model.loan import Loan
from model.user import User

BOOKS_DATA_PATH = 'data/books.csv'
LOANS_DATA_PATH = 'data/loans.csv'
USERS_DATA_PATH = 'data/users.csv'


class Library:
    def __init__(self):
        self.books = []
        self.loans = []
        self.users = []
        self.logged_user = User()
        if os.path.exists(BOOKS_DATA_PATH):
            self.load_books()
        if os.path.exists(LOANS_DATA_PATH):
            self.load_loans()
        if os.path.exists(USERS_DATA_PATH):
            self.load_users()
        # else:
        #     self.set_initial_user()

    # def set_initial_user(self):
    #     self.save_user('admin', '1234', 'True')

    def load_users(self):
        with open(USERS_DATA_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)
            for row in reader:
                user = User(row[0], row[1], row[2])
                self.users.append(user)

    def load_books(self):
        with open(BOOKS_DATA_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)
            for row in reader:
                book = Book(row[0], row[1], row[2])
                self.books.append(book)

    def load_loans(self):
        with open(LOANS_DATA_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)
            for row in reader:
                loan = Loan(row[0], row[1], row[2], row[3])
                self.loans.append(loan)

    def authenticate(self, username, password, authentication_level):
        for user in self.users:
            if user.username == username:
                if authentication_level and user.librarian != 'True':
                    return LoginOutcome.NOT_LIBRARIAN
                if user.password == password:
                    self.logged_user = user
                    return LoginOutcome.LOGIN_SUCCESS
                return LoginOutcome.INVALID_PASSWORD
        return LoginOutcome.INVALID_USERNAME

    def get_available_books(self):
        available_books = [book for book in self.books if not any(loan.title == book.title for loan in self.loans)]
        return available_books

    def get_loaned_books(self):
        loaned_books = [book for book in self.books if any(loan.title == book.title for loan in self.loans)]
        return loaned_books

    def get_loaned_by_user(self):
        loaned_books = [book for book in self.books if any(
            loan.title == book.title for loan in self.loans if loan.username == self.logged_user.username)]
        return loaned_books

    def get_booked_books(self):
        booked_books = [book for book in self.books if any(
            loan.title == book.title for loan in self.loans if loan.booked_by)]
        return booked_books

    def get_booked_by_user(self):
        booked_books = [book for book in self.books if any(
            loan.title == book.title for loan in self.loans if loan.booked_by == self.logged_user.username)]
        return booked_books

    def add_book(self, title, author, keywords):
        book = Book(title, author, keywords)
        if not book.title or not book.author or not book.keywords:
            return AddBookOutcome.BOOK_NOT_NULL
        if book in self.books:
            return AddBookOutcome.BOOK_EXISTS
        self.books.append(book)
        return AddBookOutcome.ADD_BOOK_SUCCESS

    def add_loan(self, book):
        for loaned in self.loans:
            if loaned.title == book.title:
                return LoanOutcome.ALREADY_BORROWED
        if book in self.books:
            loan = Loan(book.title, self.logged_user.username)
            self.loans.append(loan)
            return LoanOutcome.BORROW_SUCCESS
        else:
            return LoanOutcome.NOT_AVAILABLE

    def add_reservation(self, book):
        for loan in self.loans:
            if loan.title == book.title:
                if loan.booked_by is None:
                    loan.booked_by = self.logged_user.username
                    return ReserveOutcome.RESERVE_SUCCESS
                else:
                    return ReserveOutcome.ALREADY_RESERVED
        return LoanOutcome.NOT_AVAILABLE

    @staticmethod
    def _remove_by_title(items, book, outcome_success, outcome_not_found):
        for item in items:
            if item.title == book.title:
                items.remove(item)
                return outcome_success
        return outcome_not_found

    def remove_book(self, title):
        self.remove_loan(title)
        return self._remove_by_title(self.books, title, RemoveBookOutcome.REMOVE_BOOK_SUCCESS,
                                     RemoveBookOutcome.BOOK_NOT_FOUND)

    def remove_loan(self, title):
        return self._remove_by_title(self.loans, title, RemoveLoanOutcome.REMOVE_LOAN_SUCCESS,
                                     RemoveLoanOutcome.LOAN_NOT_FOUND)

    def extend_loan(self, book):
        for loan in self.loans:
            if loan.title == book.title and loan.username == self.logged_user.username:
                if loan.booked_by is not None:
                    return ReserveOutcome.RESERVED_CANNOT_EXTEND
                if loan.due_date <= date.today() + timedelta(days=30):
                    loan.due_date += timedelta(days=30)
                    return ReserveOutcome.EXTEND_SUCCESS
                else:
                    return ReserveOutcome.TOO_EARLY_TO_EXTEND
        return LoanOutcome.NOT_AVAILABLE

    def save_books(self):
        with open(BOOKS_DATA_PATH, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Title', 'Author', 'Keywords'])
            for book in self.books:
                writer.writerow([book.title, book.author, book.keywords])

    def save_loans(self):
        with open(LOANS_DATA_PATH, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Book Title', 'Username', 'Due date', 'Reserved by'])
            for loan in self.loans:
                writer.writerow([loan.title, loan.username, loan.due_date, loan.booked_by])

    def save_user(self, username, password, librarian=''):
        for user in self.users:
            if user.username == username:
                return AddUserOutcome.USER_EXISTS
        with open(USERS_DATA_PATH, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([username, password, librarian])
        return AddUserOutcome.USER_ADDED_SUCCESS

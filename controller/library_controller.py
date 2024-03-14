from model.library import Library, LoginOutcome, LoanOutcome, ReserveOutcome
from view.menu import Menu


class LibraryController:
    def __init__(self):
        self.model = Library()
        self.view = Menu()
        self.callback_menu = []

    def start(self):
        self.view.manage_menu(self.get_login_menu_options())

    # Common methods

    def login(self, authentication_level=False):
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_result = self.model.authenticate(username, password, authentication_level)
        self.view.display_message(login_result.value)
        if login_result == LoginOutcome.LOGIN_SUCCESS:
            if self.model.logged_user.librarian and authentication_level:
                self.callback_menu.append(("Back", lambda: self.view.manage_menu(self.get_librarian_menu_options())))
            else:
                self.callback_menu.append(("Back", lambda: self.view.manage_menu(self.get_member_menu_options())))
            self.callback_menu[0][1]()

    def perform_action_by_title(self, collection, action):
        title = input("Enter the title of the book: ")
        book = next((book for book in collection if book.title == title), None)
        if book:
            action(book)
        else:
            self.view.display_message("Not found.")

    def search_by_title(self):
        phrase = input("Search: ")
        return [book for book in self.model.books if phrase.lower() in book.title.lower()]

    def search_by_author(self):
        phrase = input("Search: ")
        return [book for book in self.model.books if phrase.lower() in book.title.lower()]

    def search_by_keywords(self):
        phrase = input("Search: ")
        return [book for book in self.model.books if phrase.lower() in book.keywords.lower()]

    def logout(self):
        self.model.save_books()
        self.model.save_loans()
        self.model = Library()
        self.callback_menu = []
        self.view.display_message("You have been successfully logged out.")
        self.view.manage_menu(self.get_login_menu_options())

    # Member methods

    def borrow_from_list(self):
        self.view.display_book_menu(self.model.get_available_books(), self.borrow_book, self.callback_menu)

    def borrow_by_title(self):
        self.perform_action_by_title(self.model.get_available_books(), self.borrow_book)

    def loan_from_list(self):
        self.view.display_book_menu([loaned_book for loaned_book in self.model.get_loaned_books() if
                                     loaned_book not in self.model.get_loaned_by_user()], self.reserve_book,
                                    self.callback_menu)

    def loan_by_title(self):
        self.perform_action_by_title([loaned_book for loaned_book in self.model.get_loaned_books() if
                                      loaned_book not in self.model.get_loaned_by_user()], self.reserve_book)

    def extend_from_list(self):
        self.view.display_book_menu([loaned_book for loaned_book in self.model.get_loaned_by_user() if
                                     loaned_book not in self.model.get_booked_books()], self.extend_loan,
                                    self.callback_menu)

    def extend_by_title(self):
        self.perform_action_by_title([loaned_book for loaned_book in self.model.get_loaned_by_user() if
                                      loaned_book not in self.model.get_booked_books()], self.extend_loan)

    def borrow_book(self, book):
        borrow_result = self.model.add_loan(book)
        self.handle_borrow_result(borrow_result, book)

    def handle_borrow_result(self, borrow_result, book):
        message = borrow_result.value.format(title=book.title, username=self.model.logged_user.username)
        self.view.display_message(message)
        if borrow_result == LoanOutcome.BORROW_SUCCESS:
            self.view.manage_menu(self.get_member_menu_options())
        else:
            self.view.manage_menu(self.get_borrow_menu_options())

    def reserve_book(self, book):
        reserve_result = self.model.add_reservation(book)
        self.handle_reserve_result(reserve_result, book)

    def handle_reserve_result(self, reserve_result, book):
        message = reserve_result.value.format(title=book.title, username=self.model.logged_user.username)
        self.view.display_message(message)
        if reserve_result == ReserveOutcome.RESERVE_SUCCESS:
            self.view.manage_menu(self.get_member_menu_options())
        else:
            self.view.manage_menu(self.get_reserve_menu_options())

    def extend_loan(self, book):
        extend_result = self.model.extend_loan(book)
        self.handle_extend_result(extend_result, book)

    def handle_extend_result(self, extend_result, book):
        message = extend_result.value.format(title=book.title, username=self.model.logged_user.username)
        self.view.display_message(message)
        if extend_result == ReserveOutcome.EXTEND_SUCCESS:
            self.view.manage_menu(self.get_member_menu_options())
        else:
            self.view.manage_menu(self.get_extend_menu_options())

    # Librarian methods

    def accept_from_list(self):
        self.view.display_loan_menu(self.model.loans, self.remove_loan, self.callback_menu)

    def accept_by_title(self):
        self.perform_action_by_title(self.model.loans, self.remove_loan)

    def remove_book_from_list(self):
        self.view.display_book_menu(self.model.books, self.remove_book, self.callback_menu)

    def remove_book_by_title(self):
        self.perform_action_by_title(self.model.books, self.remove_book)

    def add_book(self):
        title = input("Enter title: ")
        author = input("Enter author: ")
        keywords = input("Enter comma-separated keywords: ")
        add_book_result = self.model.add_book(title, author, keywords)
        self.view.display_message(add_book_result.value.format(title=title))
        self.view.manage_menu(self.get_librarian_menu_options())

    def remove_book(self, book):
        remove_book_result = self.model.remove_book(book)
        self.view.display_message(remove_book_result.value.format(title=book.title))
        self.view.manage_menu(self.get_remove_book_menu_options())

    def remove_loan(self, book):
        remove_loan_result = self.model.remove_loan(book)
        self.view.display_message(remove_loan_result.value.format(title=book.title))
        self.view.manage_menu(self.get_accept_return_menu_options())

    def add_member(self):
        name = input("Enter user name: ")
        password = input("Enter user password: ")
        add_user_result = self.model.save_user(name, password)
        self.view.display_message(add_user_result.value.format(username=name))
        self.view.manage_menu(self.get_librarian_menu_options())

    # Common menu options

    def get_login_menu_options(self):
        return [
            ("Login as member", lambda: self.login),
            ("Login as librarian", lambda: self.login(authentication_level=True)),
        ]

    def get_search_menu(self):
        return [
            ("Search by title", lambda: self.view.display_books(self.search_by_title())),
            ("Search by author", lambda: self.view.display_books(self.search_by_author())),
            ("Search by keywords", lambda: self.view.display_books(self.search_by_keywords())),
        ] + self.callback_menu

    # Member menu options

    def get_member_menu_options(self):
        return [
            ("Borrow a book", lambda: self.view.manage_menu(self.get_borrow_menu_options())),
            ("Reserve a book that is on loan", lambda: self.view.manage_menu(self.get_reserve_menu_options())),
            ("Extend a loan", lambda: self.view.manage_menu(self.get_extend_menu_options())),
            ("Browse the catalogue", lambda: self.view.manage_menu(self.get_search_menu())),
            ("Logout", self.logout),
        ]

    def get_borrow_menu_options(self):
        return [
            ("Browse from a list", self.borrow_from_list),
            ("Enter the title of a book to borrow", self.borrow_by_title),
        ] + self.callback_menu

    def get_reserve_menu_options(self):
        return [
            ("Browse from a list", self.loan_from_list),
            ("Enter the title of a book to reserve", self.loan_by_title),
        ] + self.callback_menu

    def get_extend_menu_options(self):
        return [
            ("Browse from a list", self.extend_from_list),
            ("Enter the title of a book to extend", self.extend_by_title),
        ] + self.callback_menu

    # Librarian menu options

    def get_librarian_menu_options(self):
        return [
            ("Accept the return of a book", lambda: self.view.manage_menu(self.get_accept_return_menu_options())),
            ("Add a book", self.add_book),
            ("Remove a book", lambda: self.view.manage_menu(self.get_remove_book_menu_options())),
            ("Add a member", self.add_member),
            ("Browse the catalogue", lambda: self.view.manage_menu(self.get_search_menu())),
            ("Logout", self.logout),
        ]

    def get_accept_return_menu_options(self):
        return [
            ("Browse from a list", self.accept_from_list),
            ("Enter the title of a returned book", self.accept_by_title),
        ] + self.callback_menu

    def get_remove_book_menu_options(self):
        return [
            ("Browse from a list", self.remove_book_from_list),
            ("Enter the title of a book to remove", self.remove_book_by_title),
        ] + self.callback_menu

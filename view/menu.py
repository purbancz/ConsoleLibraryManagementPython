# import os


class Menu:

    @staticmethod
    def display_message(message, **kwargs):
        print(message.format(**kwargs))

    # def clear_console(self):
    #     command = 'clear' if 'MSYSTEM' in os.environ or 'CYGWIN' in os.environ or os.name != 'nt' else 'cls'
    #     os.system(command)

    def print_menu(self, menu_options):
        # self.clear_console()
        for count, option in enumerate(menu_options):
            print(str(count + 1) + ' ' + option[0])

    def get_user_choice(self, menu_options):
        while True:
            choice = input("Select an option: ")
            try:
                if int(choice) < 0:
                    raise IndexError
                function = menu_options[int(choice) - 1][1]
                return function()
            except ValueError:
                print("Value must be integer")
            except IndexError:
                print(f"Value must be in range 1-{len(menu_options)}")

    def manage_menu(self, menu_options):
        while True:
            self.print_menu(menu_options)
            choice = self.get_user_choice(menu_options)
            if callable(choice):
                choice()

    @staticmethod
    def display_books(books):
        if not books:
            print("No match.")
        else:
            print("{:<40} {:<30} {:<30}".format('Title', 'Author', 'Keywords'))
            for book in books:
                print("{:<40} {:<30} {:<30}".format(book.title, book.author, book.keywords))

    def display_data_dependent_menu(self, collection, action, callback_menu=None):
        if callback_menu is None:
            callback_menu = []
        print("Choose from the list:")
        menu = []
        for item in collection:
            menu.append(
                ("{:<40} {:<30} {:<30}".format(*[getattr(item, attr) for attr in item._fields]),
                 lambda chosen_item=item: action(chosen_item))
            )
        if not menu:
            print("No items available.")
            # self.manage_menu(self.callback_menu)
        self.manage_menu(menu + callback_menu)

    def display_book_menu(self, books, action, callback_menu=None):
        if callback_menu is None:
            callback_menu = []
        print("Choose from the list:")
        book_menu = []
        for book in books:
            book_menu.append(
                ("{:<40} {:<30} {:<30}".format(book.title, book.author, book.keywords),
                 lambda chosen_book=book: action(chosen_book))
            )
        if not book_menu:
            print("No books available.")
            # self.manage_menu(self.callback_menu)
        self.manage_menu(book_menu + callback_menu)

    def display_loan_menu(self, loans, action, callback_menu=None):
        if callback_menu is None:
            callback_menu = []
        print("Choose from the list:")
        loan_menu = []
        for loan in loans:
            loan_menu.append(
                ("{:<40} {:<30} {:<15}".format(loan.title, loan.username, loan.due_date),
                 lambda chosen_loan=loan: action(chosen_loan))
            )
        if not loan_menu:
            print("No loans available.")
            # self.manage_menu(self.callback_menu)
        self.manage_menu(loan_menu + callback_menu)

    # def display_yes_no_menu(self, yes_action, no_action):
    #     yes_no_menu = [
    #         ("Yes", yes_action),
    #         ("No", no_action)
    #     ]
    #     self.manage_menu(yes_no_menu)

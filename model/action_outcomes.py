from enum import Enum


class LoginOutcome(Enum):
    LOGIN_SUCCESS = "Login successful!"
    INVALID_PASSWORD = "Invalid password."
    INVALID_USERNAME = "Invalid username."
    NOT_LIBRARIAN = "User is not a librarian."


class LoanOutcome(Enum):
    BORROW_SUCCESS = "Book '{title}' has been successfully borrowed by {username}."
    ALREADY_BORROWED = "Book '{title}' is already borrowed."
    NOT_AVAILABLE = "Book '{title}' is not available."


class ReserveOutcome(Enum):
    RESERVE_SUCCESS = "Book '{title}' has been successfully reserved by {username}."
    ALREADY_RESERVED = "Book '{title}' is already reserved."
    EXTEND_SUCCESS = "Loan for '{title}' has been successfully extended by {username}."
    RESERVED_CANNOT_EXTEND = "Book '{title}' is reserved by another user and cannot be extended."
    TOO_EARLY_TO_EXTEND = "It's too early to extend the loan for '{title}'."


class AddBookOutcome(Enum):
    ADD_BOOK_SUCCESS = "Book '{title}' has been successfully added to library."
    BOOK_EXISTS = "Book '{title}' already exists."
    BOOK_NOT_NULL = "Book data cannot be empty."


class RemoveBookOutcome(Enum):
    REMOVE_BOOK_SUCCESS = "Book '{title}' has been successfully removed from the library."
    BOOK_NOT_FOUND = "Book '{title}' not found in the library."


class RemoveLoanOutcome(Enum):
    REMOVE_LOAN_SUCCESS = "Loan for '{title}' has been successfully removed."
    LOAN_NOT_FOUND = "Loan for '{title}' not found."


class AddUserOutcome(Enum):
    USER_ADDED_SUCCESS = "User '{username}' has been successfully added."
    USER_EXISTS = "User '{username}' already exists."

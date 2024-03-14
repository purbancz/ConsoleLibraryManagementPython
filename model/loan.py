from datetime import date, timedelta


class Loan:
    def __init__(self, title, username, due_date=date.today() + timedelta(days=30), booked_by=None):
        self.title = title
        self.username = username
        self.due_date = due_date
        self.booked_by = booked_by

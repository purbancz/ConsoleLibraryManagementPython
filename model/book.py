class Book:
    def __init__(self, title, author, keywords):
        self.title = title
        self.author = author
        self.keywords = keywords

    def __eq__(self, other):
        return self.title == other.title

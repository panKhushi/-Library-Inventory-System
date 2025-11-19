import csv

class Book:
    books_file = "books.csv"
    all_books = {}       
    borrow_count = {}    

    def __init__(self, book_id, title, author, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.available = available

    def to_list(self):
        return [self.book_id, self.title, self.author, str(self.available)]

    @classmethod
    def load_books(cls):
        try:
            with open(cls.books_file, "r", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    book_id, title, author, available = row
                    book = Book(book_id, title, author, available == "True")
                    cls.all_books[book_id] = book
                    cls.borrow_count.setdefault(book_id, 0)
        except FileNotFoundError:
            pass

    @classmethod
    def save_books(cls):
        with open(cls.books_file, "w", newline="") as f:
            writer = csv.writer(f)
            for book in cls.all_books.values():
                writer.writerow(book.to_list())

    @classmethod
    def most_borrowed(cls):
        if not cls.borrow_count:
            return None
        book_id = max(cls.borrow_count, key=cls.borrow_count.get)
        return cls.all_books.get(book_id)


class Member:
    members_file = "members.csv"
    all_members = {}  

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def to_list(self):
        borrowed = "|".join(self.borrowed_books)
        return [self.member_id, self.name, borrowed]

    @classmethod
    def load_members(cls):
        try:
            with open(cls.members_file, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    member_id, name, borrowed = row
                    member = Member(member_id, name)
                    member.borrowed_books = borrowed.split("|") if borrowed else []
                    cls.all_members[member_id] = member
        except FileNotFoundError:
            pass

    @classmethod
    def save_members(cls):
        with open(cls.members_file, "w", newline="") as f:
            writer = csv.writer(f)
            for member in cls.all_members.values():
                writer.writerow(member.to_list())



class Library:

    @staticmethod
    def add_book(book_id, title, author):
        book = Book(book_id, title, author)
        Book.all_books[book_id] = book
        Book.save_books()

    @staticmethod
    def add_member(member_id, name):
        member = Member(member_id, name)
        Member.all_members[member_id] = member
        Member.save_members()

    @staticmethod
    def borrow_book(member_id, book_id):
        member = Member.all_members.get(member_id)
        book = Book.all_books.get(book_id)

        if not member:
            return "Member not found"
        if not book:
            return "Book not found"
        if not book.available:
            return "Book is already borrowed"

        book.available = False
        member.borrowed_books.append(book_id)

        # Analytics update
        Book.borrow_count[book_id] = Book.borrow_count.get(book_id, 0) + 1

        Book.save_books()
        Member.save_members()

        return f"{member.name} borrowed '{book.title}'"

    @staticmethod
    def return_book(member_id, book_id):
        member = Member.all_members.get(member_id)
        book = Book.all_books.get(book_id)

        if not member:
            return "Member not found"
        if not book:
            return "Book not found"
        if book_id not in member.borrowed_books:
            return "This book was not borrowed by the member"

        book.available = True
        member.borrowed_books.remove(book_id)

        Book.save_books()
        Member.save_members()

        return f"'{book.title}' returned successfully"



Book.load_books()
Member.load_members()

def menu():
    print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
    print("1. Add Book")
    print("2. Add Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Show Most Borrowed Book")
    print("6. Exit")

while True:
    menu()
    choice = input("Enter choice: ")

    if choice == "1":
        book_id = input("Enter Book ID: ")
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        Library.add_book(book_id, title, author)
        print("✔ Book added successfully")

    elif choice == "2":
        member_id = input("Enter Member ID: ")
        name = input("Enter Member Name: ")
        Library.add_member(member_id, name)
        print("✔ Member added successfully")

    elif choice == "3":
        member_id = input("Enter Member ID: ")
        book_id = input("Enter Book ID: ")
        print(Library.borrow_book(member_id, book_id))

    elif choice == "4":
        member_id = input("Enter Member ID: ")
        book_id = input("Enter Book ID: ")
        print(Library.return_book(member_id, book_id))

    elif choice == "5":
        book = Book.most_borrowed()
        if book:
            print(f"📘 Most Borrowed Book: {book.title} by {book.author}")
        else:
            print("No books borrowed yet.")

    elif choice == "6":
        print("Exiting program...")
        break

    else:
        print("Invalid choice! Try again.")

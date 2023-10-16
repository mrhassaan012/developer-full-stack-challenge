import random

from sqlalchemy.orm import sessionmaker

from auth import get_password_hash
from database import Base, engine
from models import Author, Book, User

# Define your sample data
sample_user = {"id": 1, "username": "testuser", "hashed_password": get_password_hash("testuser123")}

sample_authors = [
    {"id": 1, "name": "George R. R. Martin"},
    {"id": 2, "name": "J.K. Rowling"},
    {"id": 3, "name": "Stephen King"},
    {"id": 4, "name": "Agatha Christie"},
    {"id": 5, "name": "J.R.R. Tolkien"},
    {"id": 6, "name": "Jane Austen"},
    {"id": 7, "name": "Leo Tolstoy"},
    {"id": 8, "name": "F. Scott Fitzgerald"},
    {"id": 9, "name": "Harper Lee"},
    {"id": 10, "name": "Mark Twain"},
    {"id": 11, "name": "Charles Dickens"},
    {"id": 12, "name": "Toni Morrison"},
    {"id": 13, "name": "Gabriel García Márquez"},
    {"id": 14, "name": "Ernest Hemingway"},
    {"id": 15, "name": "Emily Brontë"},
    {"id": 16, "name": "Charlotte Brontë"},
    {"id": 17, "name": "Fyodor Dostoevsky"},
    {"id": 18, "name": "Jules Verne"},
    {"id": 19, "name": "H.G. Wells"},
    {"id": 20, "name": "Agnes Gonxha Bojaxhiu"},
    {"id": 21, "name": "Maya Angelou"},
    {"id": 22, "name": "Pablo Neruda"},
    {"id": 23, "name": "Gabrielle Bonheur Chanel"},
    {"id": 24, "name": "Virginia Woolf"},
    {"id": 25, "name": "Aldous Huxley"},
    {"id": 26, "name": "Herman Melville"},
    {"id": 27, "name": "Rabindranath Tagore"},
    {"id": 28, "name": "Friedrich Nietzsche"},
    {"id": 29, "name": "Jane Goodall"},
    {"id": 30, "name": "Oscar Wilde"},
    # Add more authors as needed with their corresponding IDs
]


sample_books = [
    {"name": "A Game of Thrones", "author_id": 1},
    {"name": "A Clash of Kings", "author_id": 1},
    {"name": "A Storm of Swords", "author_id": 1},
    {"name": "Harry Potter and the Sorcerer's Stone", "author_id": 2},
    {"name": "Harry Potter and the Chamber of Secrets", "author_id": 2},
    {"name": "Harry Potter and the Prisoner of Azkaban", "author_id": 2},
    {"name": "It", "author_id": 3},
    {"name": "The Shining", "author_id": 3},
    {"name": "The Lord of the Rings: The Fellowship of the Ring", "author_id": 4},
    {"name": "The Lord of the Rings: The Two Towers", "author_id": 4},
    {"name": "The Lord of the Rings: The Return of the King", "author_id": 4},
    {"name": "Murder on the Orient Express", "author_id": 5},
    {"name": "War and Peace", "author_id": 6},
    {"name": "Pride and Prejudice", "author_id": 7},
    {"name": "The Adventures of Huckleberry Finn", "author_id": 8},
    {"name": "Great Expectations", "author_id": 9},
    {"name": "Moby-Dick", "author_id": 10},
    {"name": "The Great Gatsby", "author_id": 11},
    {"name": "The Old Man and the Sea", "author_id": 12},
    {"name": "1984", "author_id": 13},
    {"name": "The Handmaid's Tale", "author_id": 14},
    {"name": "To Kill a Mockingbird", "author_id": 15},
    {"name": "Twenty Thousand Leagues Under the Sea", "author_id": 16},
    {"name": "Frankenstein", "author_id": 17},
    {"name": "The War of the Worlds", "author_id": 18},
    {"name": "Wuthering Heights", "author_id": 19},
    {"name": "The Odyssey", "author_id": 20},
]


# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


# Seed the database with sample data
def seed_data():
    # Create the user
    user = User(**sample_user)
    db.add(user)

    # Create the authors
    for author_data in sample_authors:
        author = Author(**author_data)
        db.add(author)

    # Create the books
    for book_data in sample_books:
        num_pages = random.randint(500, 1000)
        book = Book(**book_data, num_pages=num_pages)
        db.add(book)

    db.commit()


if __name__ == "__main__":
    seed_data()

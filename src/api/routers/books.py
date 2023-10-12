from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from auth import user_dependency
from database import get_db
from models import Book

router = APIRouter()

# current_user: user_dependency,


@router.post("/", response_model=schemas.Book)
def add_book(book: schemas.Book, db: Session = Depends(get_db)):
    db_book = Book(name=book.name, author_id=book.author_id)
    db.add(db_book)
    db.commit()
    return db_book


@router.get("/", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()

    return books


@router.get("/{book_id}", response_model=schemas.Book)
def get_one_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="book not found")

    return book


# @router.patch("/{book_id}", response_model=schemas.Book)
# def update_book(book_id: int, book: schemas.UpdateBook, db: Session = Depends(get_db)):
#     db_book = db.get(Book, book_id)
#     if not db_book:
#         raise HTTPException(status_code=404, detail="Book not found")

#     book_data = book.dict(exclude_unset=True)
#     for key, value in book_data.items():
#         setattr(db_book, key, value)

#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#     return db_book

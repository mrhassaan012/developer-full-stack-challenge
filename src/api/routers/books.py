from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

import schemas
from auth import user_dependency
from database import get_db
from models import Author, Book

router = APIRouter()

# current_user: user_dependency,


def verify_author_id(db, author_id):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")


@router.post("/", response_model=schemas.BookWithID)
def add_book(current_user: user_dependency, book: schemas.BookUpsert, db: Session = Depends(get_db)):
    # Verify that the author exists
    verify_author_id(db, book.author_id)

    db_book = Book(name=book.name, author_id=book.author_id, num_pages=book.num_pages)
    db.add(db_book)
    db.commit()
    return db_book


@router.delete("/{book_id}", response_model=schemas.BookWithID)
def delete_book(current_user: user_dependency, book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).options(joinedload(Book.author)).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()

    return db_book


@router.get("/", response_model=schemas.PaginationResponse[schemas.Book])
def get_books(current_user: user_dependency, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    total_count = db.query(Book).count()
    books = db.query(Book, Author).join(Author).order_by(Book.id.desc()).offset(skip).limit(limit).all()
    books_with_authors = [
        {"id": book.id, "name": book.name, "author": author, "num_pages": book.num_pages} for book, author in books
    ]

    current_page = (skip // limit) + 1
    total_pages = (total_count - 1) // limit + 1
    has_next_page = skip + limit < total_count
    has_prev_page = skip > 0

    return schemas.PaginationResponse[schemas.Book](
        total_count=total_count,
        current_page=current_page,
        total_pages=total_pages,
        has_next_page=has_next_page,
        has_prev_page=has_prev_page,
        data=books_with_authors,
    )


@router.get("/{book_id}", response_model=schemas.Book)
def get_one_book(current_user: user_dependency, book_id: int, db: Session = Depends(get_db)):
    result = db.query(Book, Author).join(Author).filter(Book.id == book_id).first()

    print(result)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")

    book, author = result

    return {
        "id": book.id,
        "name": book.name,
        "author": author,
        "num_pages": book.num_pages,
    }


@router.patch("/{book_id}", response_model=schemas.BookWithID)
def update_book(current_user: user_dependency, book_id: int, book: schemas.BookUpsert, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Verify that the author exists
    if "author_id" in book.dict():
        verify_author_id(db, book.author_id)

    book_data = book.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/search/", response_model=list[schemas.Book])
def search_books(current_user: user_dependency, query: str, db: Session = Depends(get_db)):
    books = (
        db.query(Book, Author)
        .filter(
            or_(Book.name.ilike(f"%{query}%"), Author.name.ilike(f"%{query}%")),
        )
        .join(Book.author)
        .all()
    )

    print("books-----------", books)

    results = []
    for book, author in books:
        result = {
            "id": book.id,
            "name": book.name,
            "author": {
                "id": author.id,
                "name": author.name,
            },
            "num_pages": book.num_pages,
        }
        results.append(result)

    return results


@router.get("/{author_id}", response_model=schemas.PaginationResponse[schemas.Book])
def get_books_by_author(
    current_user: user_dependency,
    author_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    total_count = db.query(Book).count()
    books = db.query(Book, Author).join(Author).offset(skip).limit(limit).filter(Author.id == author_id)
    books_with_authors = [{"id": book.id, "name": book.name, "author": author} for book, author in books]

    current_page = (skip // limit) + 1
    total_pages = (total_count - 1) // limit + 1
    has_next_page = skip + limit < total_count
    has_prev_page = skip > 0

    return schemas.PaginationResponse[schemas.Book](
        total_count=total_count,
        current_page=current_page,
        total_pages=total_pages,
        has_next_page=has_next_page,
        has_prev_page=has_prev_page,
        data=books_with_authors,
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

import schemas
from auth import user_dependency
from database import get_db
from models import Author, Book

router = APIRouter()

# current_user: user_dependency,


@router.post("/", response_model=schemas.AuthorWithID)
def add_author(author: schemas.Author, db: Session = Depends(get_db)):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    return db_author


@router.delete("/{author_id}", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    # Check if the author with the given ID exists
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Delete the author
    db.delete(db_author)
    db.commit()

    return db_author


@router.get("/", response_model=schemas.PaginationResponse[schemas.AuthorWithID])
def get_authors(current_user: user_dependency, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = (
        db.query(Author, func.count(Book.id).label("book_count"))
        .outerjoin(Book)
        .group_by(Author.id)
        .offset(skip)
        .limit(limit)
    )

    authors = query.all()
    total_count = db.query(Author).count()

    current_page = (skip // limit) + 1
    total_pages = (total_count - 1) // limit + 1
    has_next_page = skip + limit < total_count
    has_prev_page = skip > 0

    return schemas.PaginationResponse[schemas.AuthorWithID](
        total_count=total_count,
        current_page=current_page,
        total_pages=total_pages,
        has_next_page=has_next_page,
        has_prev_page=has_prev_page,
        data=[
            schemas.AuthorWithID(id=author.id, name=author.name, book_count=book_count)
            for author, book_count in authors
        ],
    )


@router.get("/{author_id}", response_model=schemas.AuthorWithID)
def get_one_authors(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="author not found")

    return author


@router.put("/{author_id}", response_model=schemas.AuthorWithID)
def update_author(author_id: int, author: schemas.Author, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()

    if not db_author:
        raise HTTPException(status_code=404, detail="author not found")

    # Update the author's information.
    for field, value in author.dict().items():
        setattr(db_author, field, value)

    db.commit()
    return db_author


@router.get("/search/", response_model=list[schemas.AuthorWithID])  # Assuming you have a BookWithID schema
def search_authors(query: str, db: Session = Depends(get_db)):
    authors = (
        db.query(Author, func.count(Book.id).label("book_count"))
        .outerjoin(Book)
        .filter(Author.name.ilike(f"%{query}%"))
        .group_by(Author.id)
        .all()
    )

    # Create a list of AuthorWithID objects with book_count
    authors_with_id = [
        schemas.AuthorWithID(id=author.id, name=author.name, book_count=book_count) for author, book_count in authors
    ]

    return authors_with_id

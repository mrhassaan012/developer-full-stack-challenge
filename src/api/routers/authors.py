from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from auth import user_dependency
from database import get_db
from models import Author

router = APIRouter()

# current_user: user_dependency,


@router.post("/", response_model=schemas.AuthorWithID)
def add_author(author: schemas.Author, db: Session = Depends(get_db)):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    return db_author


@router.get("/", response_model=list[schemas.AuthorWithID])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()

    return authors


@router.get("/{author_id}", response_model=schemas.AuthorWithID)
def get_one_authors(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="author not found")

    return author

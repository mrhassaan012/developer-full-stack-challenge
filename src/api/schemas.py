from typing import Generic, Optional, TypeVar

from pydantic import BaseModel


class Author(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AuthorWithID(Author):
    id: int
    book_count: int | None


class Book(BaseModel):
    name: str
    author: Author

    class Config:
        orm_mode = True


class BookUpsert(BaseModel):
    name: str | None = None
    author_id: int | None = None


class BookWithID(Book):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateUserRequest(BaseModel):
    username: str
    password: str


DataT = TypeVar("DataT")


class PaginationResponse(BaseModel, Generic[DataT]):
    total_count: int
    current_page: int
    total_pages: int
    has_next_page: bool
    has_prev_page: bool
    data: list[DataT]

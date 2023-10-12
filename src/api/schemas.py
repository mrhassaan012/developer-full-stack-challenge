from pydantic import BaseModel


class Author(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AuthorWithID(Author):
    id: int


class Book(BaseModel):
    name: str
    author_id: Author

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateUserRequest(BaseModel):
    username: str
    password: str

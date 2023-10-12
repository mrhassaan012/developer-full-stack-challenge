from typing import Annotated

from fastapi import Depends, FastAPI

import models
from auth import get_current_user
from auth import router as auth_router
from database import engine
from routers.authors import router as authors_router
from routers.books import router as books_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(
    books_router,
    prefix="/books",
    tags=["Books"],
    responses={418: {"description": "Books"}},
)
app.include_router(
    authors_router,
    prefix="/authors",
    tags=["Authors"],
    responses={418: {"description": "Authors"}},
)

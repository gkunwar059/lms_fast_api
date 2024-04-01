import uvicorn
from fastapi import Depends, FastAPI, status, HTTPException, exceptions
from pydantic import BaseModel, config
from sqlalchemy.exc import IntegrityError
from error_message import ErrorMessages
from models import (
    Member,
    Book,
    Magazine,
    Publisher,
    Category,
    Session,
    session,
    MemberBook,
    MemberMagazine,
    Record,
    Librarian,
)
from typing import Annotated
from auth.jwt_bearer import Librarian_JwtBearer, Member_JwtBearer
from auth.jwt_handler import Auth
from starlette.middleware.base import BaseHTTPMiddleware

from logger import logger
from middleware import log_middleware


app = FastAPI(
    title="Library Management System ",
)
app.add_middleware(BaseHTTPMiddleware,dispatch=log_middleware)
# app = FastAPI()

class MemberModel(BaseModel):
    name: str
    member_type: str
    email: str
    password: str
    address: str
    contact_no: int


class LoginModel(BaseModel):
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test@gmail.com",
                    "password": "password@1234",
                }
            ]
        }
    }


class BookModel(BaseModel):
    isbn: int
    title: str
    author: str
    price: int
    publisher_id: int
    category_id: int



class MagazineModel(BaseModel):
    issn: int
    title: str
    editor: str
    price: int
    publisher_id: int
    category_id: int

class PublisherModel(BaseModel):
    name: str
    contact_no: str
    address: str

class CategoryModel(BaseModel):
    name: str


class BorrowBookModel(BaseModel):
    isbn: int
    email: str


class ReturnBookModel(BaseModel):
    isbn: int
    email: str


class BorrowMagazineBookModel(BaseModel):
    issn: int
    email: str


class ReturnMagazineBookModel(BaseModel):
    issn: int
    email: str

logger.info("Starting API............")



@app.get("/", tags=["Home"])
async def home():
    return {
        "Members": "/members",
        "Books": "/books",
        "Publisher": "/publisher",
        "Category": "/category",
    }


#   member
@app.get(
    "/members/{email}", tags=["Member"], dependencies=[Depends(Member_JwtBearer())]
)
async def get_member(email):
    logger.info("Request to index page !")
    return Member.get_member(email)


@app.get("/members/", tags=["Member"], dependencies=[Depends(Member_JwtBearer())])
async def show_all_members(page_num: int = 1, page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size

    member = Member.get_all_members()
    response = {
        "member": member[start:end],
        "total": len(member),
        "count": page_size,
        "pagination": {},
    }

    if end > len(member):
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"][
                "previous"
            ] = f"/members?page_num={page_num-1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None

    else:
        if page_num > 1:
            response["pagination"][
                "previous"
            ] = f"/members?page_num={page_num-1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"][
            "next"
        ] = f"/members?page_num={page_num+1}&page_size={page_size}"

    return response


@app.post("/member/", tags=["Member"], status_code=status.HTTP_201_CREATED)
async def add_members(item: MemberModel):
    try:
        new_member = Member.add_member(
            item.name,
            item.member_type,
            item.email,
            item.password,
            item.address,
            item.contact_no,
        )
        return new_member

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Book
@app.get("/books/{isbn}", tags=["Book"], dependencies=[Depends(Member_JwtBearer())])
async def get_book(isbn):
    return Book.get_book(isbn=isbn)



@app.get("/books/", tags=["Book"], dependencies=[Depends(Librarian_JwtBearer())])
async def show_all_books():
    return Book.get_all_books()


@app.post(
    "/books/",
    tags=["Book"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(Librarian_JwtBearer())],
)
async def add_book(book: BookModel):
    try:
        new_book = Book.add_book(
            book.isbn,
            book.title,
            book.author,
            book.price,
            book.publisher_id,
            book.category_id,
        )
        return new_book
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post(
    "/books/borrowbook",
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
    dependencies=[Depends(Member_JwtBearer())],
)
async def borrow_book(book_borrow: BorrowBookModel):
    # instance self xa vane chai instance dekhi call garne hai ta
    book = Book.get_book(isbn=book_borrow.isbn)
    member = Member.get_member(email=book_borrow.email)

    if book and member:
        new_book_borrow = book.borrow_book(member.id)
        # return new_book_borrow
        if new_book_borrow:
            return new_book_borrow
      
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.CREDENTIALS_NOT_MATCHED,
        )


@app.post(
    "/books/returnbook",
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
    dependencies=[Depends(Member_JwtBearer())],
)
async def return_book(bookreturn: ReturnBookModel):
    book = Book.get_book(isbn=bookreturn.isbn)
    member = Member.get_member(email=bookreturn.email)

    if book and member:

        new_return_book = book.return_book(member.id)

        if new_return_book:
            return new_return_book
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessages.BOOK_ALREADY_RETURNED)

    else:
        raise HTTPException(status_code=404, detail=ErrorMessages.BOOK_OR_MEMBER_NOT_FOUND)


# for magazine
@app.get(
    "/magazines/{issn}",
    tags=["Magazine"],
    dependencies=[Depends(Librarian_JwtBearer())],
)
async def get_magazine(issn):
    # TODO: needs to rasie exception if not found
    return Magazine.get_magazine(issn=issn)


@app.get(
    "/magazines/", tags=["Magazine"], dependencies=[Depends(Librarian_JwtBearer())]
)
async def show_all_magazines():
    return Magazine.show_all_magazines()


@app.post(
    "/magazine",
    tags=["Magazine"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(Librarian_JwtBearer())],
)
async def add_magazine(magazine: MagazineModel):
    try:

        new_magazine = Magazine.add_magazine(
            magazine.issn,
            magazine.title,
            magazine.price,
            magazine.editor,
            magazine.publisher_id,
            magazine.category_id,
        )
        return new_magazine
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=ErrorMessages.DUPLICATE_ISBN)
    
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


# borrow magazine
@app.post(
    "/magazines/borrowmagazine",
    status_code=status.HTTP_201_CREATED,
    tags=["Magazine"],
    dependencies=[Depends(Member_JwtBearer())],
)
async def borrow_magazine(magazineborrow: BorrowMagazineBookModel):
    # try:
    magazine = Magazine.get_magazine(issn=magazineborrow.issn)
    member = Member.get_member(email=magazineborrow.email)

    if member and magazine:
        new_borrow_magazine = magazine.borrow_magazine(member.id)
        if new_borrow_magazine:
            return new_borrow_magazine

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.FAILED_TO_BORROW_MAGAZINE
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.MAGAZINE_AND_MEMBER_NOT_FOUND,
        )
   

@app.post(
    "/magazines/returnmagazine",
    tags=["Magazine"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(Member_JwtBearer())],
)
async def return_magazine(magazinereturn: ReturnMagazineBookModel):
    magazine = Magazine.get_magazine(issn=magazinereturn.issn)
    member = Member.get_member(email=magazinereturn.email)

    if member and magazine:
        new_return_magazine = magazine.return_magazine(member.id)

        if new_return_magazine:
            return new_return_magazine

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.MAGAZINE_ALREADY_RETURNED,
            )

    else:
        raise HTTPException(status_code=400, detail=ErrorMessages.MAGAZINE_NOT_FOUND)



@app.get("/publishers/{name}", tags=["Publisher"], dependencies=[Depends(Librarian_JwtBearer())])
async def get_publisher(name):
    return Publisher.get_publisher(name=name)


@app.get(
    "/publishers", tags=["Publisher"], dependencies=[Depends(Librarian_JwtBearer())]
)
async def show_all_publisher():
    return Publisher.show_all_publishers()


@app.post(
    "/publisher",
    status_code=status.HTTP_201_CREATED,
    tags=["Publisher"],
    dependencies=[Depends(Librarian_JwtBearer())],
)
async def add_publisher(publisher_item: PublisherModel):
    try:
        new_publisher = Publisher.add_publisher(
            publisher_item.name, publisher_item.contact_no, publisher_item.address
        )
        return new_publisher
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# category
@app.get("/category/{name}", tags=["Category"])
async def get_category(name):
    category = Category.get_category(name=name)
    return category.name


@app.get(
    "/categories", tags=["Category"], dependencies=[Depends(Librarian_JwtBearer())]
)
async def show_category():
    return {"result": Category.show_all_categories()}

@app.post(
    "/categories/",
    status_code=status.HTTP_201_CREATED,
    tags=["Category"],
    dependencies=[Depends(Librarian_JwtBearer())],
)
async def add_category(category: CategoryModel):
    try:
        new_category = Category.add_category(category.name)
        return new_category

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/records/{email}", tags=["Record"])
async def show_all_records(email: str):
    member = Member.get_member(email=email)
    all_my_record = Record.show_all_records(member.id)
    if all_my_record:
        return all_my_record


@app.post("/records/me/{email}", tags=["Record"])
async def show_my_records(email: str):
    member = Member.get_member(email=email)
    show_my_record = Record.show_user_record(member.id)

    if show_my_record:
        return show_my_record


# librarian
@app.get("/librarian", tags=["Librarian"])
async def get_librarian(email: str):
    new_librarian = (
        session.query(Librarian).where(Librarian.email == email).one_or_none()
    )
    return new_librarian


@app.post("/librarian/login", tags=["Librarian"])
async def login(login: LoginModel):
    librarian = (
        session.query(Librarian)
        .filter_by(email=login.email, password=login.password)
        .first()
    )
    if librarian:
        token = Auth.generate_librarian_token(email=login.email)
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_CREDENTIALS,
        )


@app.get("/librarian/refresh", tags=["Librarian"])
async def refresh_login(refresh_token: str):
    valid_token = Auth.decode_librarian_token(refresh_token)
    print(valid_token)

    if valid_token:
        return Auth.generate_librarian_token(valid_token["email"])
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.INVALID_TOKEN
        )


@app.post("/member/login", tags=["Member"])
async def login(memb_login: LoginModel):
    member = (
        session.query(Member)
        .filter_by(email=memb_login.email, password=memb_login.password)
        .first()
    )
    if member:
        token = Auth.generate_member_token(email=memb_login.email)
        return token

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_CREDENTIALS,
        )


@app.get("/member/refresh", tags=["Member"])
async def refresh_token(refresh_token: str):
    valid_token = Auth.decode_member_token(refresh_token)
    print(valid_token)

    if valid_token:
        return Auth.generate_member_token(valid_token["email"])
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.INVALID_CREDENTIALS,
        )




# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

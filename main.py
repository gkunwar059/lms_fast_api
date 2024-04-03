import uvicorn
from fastapi import Depends, FastAPI, status, HTTPException, exceptions
from pydantic import BaseModel, config
from typing import List
from sqlalchemy.exc import IntegrityError
from utils.constant_message import ConstantMessage
from models import (
    User,
    Book,
    Magazine,
    Publisher,
    Category,
    Session,
    session,
    UserBook,
    UserMagazine,
    Record,
    Role,
    Permission
)
from typing import Annotated
from auth.jwt_bearer import User_JwtBearer
from auth.jwt_handler import Auth
from starlette.middleware.base import BaseHTTPMiddleware
from auth.permission_check import RoleCheck
from utils.logger import logger
from utils.middleware import log_middleware


app = FastAPI(
    title="Library Management System ",
)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

class UserModel(BaseModel):
    name: str
    email: str
    password: str
    address: str
    contact_no: int
    role_id: int


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


class RefreshToken(BaseModel):
    refresh_token: str
    
class RoleModel(BaseModel):
    name:str
    
class PermissionModel(BaseModel):
    name:str
    permission_names:str
    
class AssignPermissionRole(BaseModel):
    permission_id:int
    role_id:int
    
class AssignUserRole(BaseModel):
    user_id:int
    role_id:int


@app.get("/", tags=["Home"])
async def home():
    return {
        "User": "/users",
        "Books": "/books",
        "Publisher": "/publisher",
        "Category": "/category",
    }


#   user
@app.get("/users/{email}", tags=["User"], dependencies=[Depends(User_JwtBearer())])
async def get_user(
    email, _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"]))
):
    logger.info("Request to index page !")
    return User.get_user(email)


@app.get("/users/", tags=["User"], dependencies=[Depends(User_JwtBearer())])
async def show_all_users(
    page_num: int = 1,
    page_size: int = 10,
    _: bool = Depends(RoleCheck(allowed_permission=["user:all"])),
):
    start = (page_num - 1) * page_size
    end = start + page_size

    user = User.get_all_users()
    response = {
        "user": user[start:end],
        "total": len(user),
        "count": page_size,
        "pagination": {},
    }


    if end > len(user):
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"][
                "previous"
            ] = f"/users?page_num={page_num-1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None


    else:
        if page_num > 1:
            response["pagination"][
                "previous"
            ] = f"/users?page_num={page_num-1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"][
            "next"
        ] = f"/users?page_num={page_num+1}&page_size={page_size}"

    return response



@app.post("/user/", tags=["User"], status_code=status.HTTP_201_CREATED)
async def add_user(item: UserModel):
    try:
        new_user = User.add_user(
            item.name,
            item.email,
            item.password,
            item.address,
            item.contact_no,
            item.role_id,
        )
        return new_user

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
















@app.post("/role/add",tags=['Role'])
async def create_role(role:RoleModel):
    role=Role.create_role(role.name)      #TODO:validation and exception are required later on 
    if role:
        return True
    else:
        return False
        
@app.post('/role/assignrole',tags=['Role'])
async def assign_role_to_user(assignrole:AssignUserRole):
    user_role=Role.assign_role_to_user(user_id=assignrole.user_id,role_id=assignrole.role_id)
    return user_role        

@app.post('/permission',tags=['Permission'])
async def create_permission(permission:PermissionModel):
    
    new_permission=Permission.create_permission(permission.name)
    return new_permission
    
    
@app.post('/permission/assignrole',tags=['Permission'])
async def assign_permission_to_role(assign_permission:AssignPermissionRole):
    role_permission=Permission.assign_permission_to_role(permission_id=assign_permission.permission_id,role_id=assign_permission.role_id)
    return role_permission



# @app.post("/roles/")
# async def create_role_with_permissions(role:PermissionModel):
#     try:
#         role = Permission.assign_role_and_permission(role.name, role.permission_names)
#         # return  role
#         print(role)
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# Book
@app.get("/book/{isbn}", tags=["Book"], dependencies=[Depends(User_JwtBearer())])
async def get_book(
    isbn, _: bool = Depends(RoleCheck(allowed_permission=["admin:all"]))
):
    return Book.get_book(isbn=isbn)


@app.get("/books/", tags=["Book"], dependencies=[Depends(User_JwtBearer())])
async def show_all_books(
    _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"]))
):
    return Book.get_all_books()


@app.post(
    "/books/",
    tags=["Book"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(User_JwtBearer())],
)
async def add_book(
    book: BookModel, _: bool = Depends(RoleCheck(allowed_permission=["admin:all"]))
):
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
    "/book/borrow",
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
    dependencies=[Depends(User_JwtBearer())],
)
async def borrow_book(
    book_borrow: BorrowBookModel,
    _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"])),
):
    # instance self xa vane chai instance dekhi call garne hai ta
    book = Book.get_book(isbn=book_borrow.isbn)
    user = User.get_user(email=book_borrow.email)

    if book and user:
        new_book_borrow = book.borrow_book(user.id)
        # return new_book_borrow
        if new_book_borrow:
            return new_book_borrow

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ConstantMessage.CREDENTIALS_NOT_MATCHED,
        )



@app.post(
    "/book/return",
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
    dependencies=[Depends(User_JwtBearer())],
)
async def return_book(
    bookreturn: ReturnBookModel,
    _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"])),
):
    book = Book.get_book(isbn=bookreturn.isbn)
    user = User.get_user(email=bookreturn.email)

    if book and user:

        new_return_book = book.return_book(user.id)

        if new_return_book:
            return new_return_book
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ConstantMessage.BOOK_ALREADY_RETURNED,
            )

    else:
        raise HTTPException(
            status_code=404, detail=ConstantMessage.BOOK_OR_USER_NOT_FOUND
        )


# for magazine
@app.get(
    "/magazine/{issn}",
    tags=["Magazine"],
    dependencies=[Depends(User_JwtBearer())],
)
async def get_magazine(
    issn, _: bool = Depends(RoleCheck(allowed_permission=["admin:all"]))
):
    # TODO: needs to rasie exception if not found
    return Magazine.get_magazine(issn=issn)


@app.get("/magazines/", tags=["Magazine"], dependencies=[Depends(User_JwtBearer())])
async def show_all_magazines(
    _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"]))
):
    return Magazine.show_all_magazines()


@app.post(
    "/magazine",
    tags=["Magazine"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(User_JwtBearer())],
)
async def add_magazine(
    magazine: MagazineModel,
    _: bool = Depends(RoleCheck(allowed_permission=["admin:all"])),
):
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ConstantMessage.DUPLICATE_ISBN,
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))











# borrow magazine
@app.post(
    "/magazine/borrow",
    status_code=status.HTTP_201_CREATED,
    tags=["Magazine"],
    dependencies=[Depends(User_JwtBearer())],
)
async def borrow_magazine(
    magazineborrow: BorrowMagazineBookModel,
    _: bool = Depends(RoleCheck(allowed_permission=["admin:all", "user:all"])),
):
    magazine = Magazine.get_magazine(issn=magazineborrow.issn)
    user = User.get_user(email=magazineborrow.email)

    if user and magazine:
        new_borrow_magazine = magazine.borrow_magazine(user.id)
        if new_borrow_magazine:
            return new_borrow_magazine

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ConstantMessage.FAILED_TO_BORROW_MAGAZINE,
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ConstantMessage.MAGAZINE_AND_USER_NOT_FOUND,
        )


@app.post(
    "/magazine/return",
    tags=["Magazine"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(User_JwtBearer())],
)
async def return_magazine(
    magazinereturn: ReturnMagazineBookModel,
    _: bool = Depends(RoleCheck(allowed_permission=["admin:all", "user:all"])),
):
    magazine = Magazine.get_magazine(issn=magazinereturn.issn)
    user = User.get_user(email=magazinereturn.email)

    if user and magazine:
        new_return_magazine = magazine.return_magazine(user.id)

        if new_return_magazine:
            return new_return_magazine

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ConstantMessage.MAGAZINE_ALREADY_RETURNED,
            )

    else:
        raise HTTPException(status_code=400, detail=ConstantMessage.MAGAZINE_NOT_FOUND)


@app.get(
    "/publisher/{name}", tags=["Publisher"], dependencies=[Depends(User_JwtBearer())]
)
async def get_publisher(
    name, _: bool = Depends(RoleCheck(allowed_permission=["admin:all"]))
):
    return Publisher.get_publisher(name=name)


@app.get("/publishers", tags=["Publisher"], dependencies=[Depends(User_JwtBearer())])
async def show_all_publisher(
    _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"]))
):
    return Publisher.show_all_publishers()


@app.post(
    "/publisher",
    status_code=status.HTTP_201_CREATED,
    tags=["Publisher"],
    dependencies=[Depends(User_JwtBearer())],
)
async def add_publisher(
    publisher_item: PublisherModel,
    _: bool = Depends(RoleCheck(allowed_permission=["admin:all"])),
):
    try:
        new_publisher = Publisher.add_publisher(
            publisher_item.name, publisher_item.contact_no, publisher_item.address
        )
        return new_publisher
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# category
@app.get("/category/{name}", tags=["Category"])
async def get_category(
    name, _: bool = Depends(RoleCheck(allowed_permission=["admin:all", "user:all"]))
):
    category = Category.get_category(name=name)
    return category.name


@app.get("/categories", tags=["Category"], dependencies=[Depends(User_JwtBearer)])
async def show_category(
    _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"]))
):

    return {"result": Category.show_all_categories()}


@app.post(
    "/category/",
    status_code=status.HTTP_201_CREATED,
    tags=["Category"],
    dependencies=[Depends(User_JwtBearer())],
)
async def add_category(
    category: CategoryModel,
    _: bool = Depends(RoleCheck(allowed_permission=["admin:all"])),
):
    try:
        new_category = Category.add_category(category.name)
        return new_category

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/records/{email}", tags=["Record"])
async def show_all_records(
    email: str,
    _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"])),
):
    user = User.get_user(email=email)
    all_my_record = Record.show_all_records(user.id)
    if all_my_record:
        return all_my_record


@app.post("/records/me/{email}", tags=["Record"])
async def show_my_records(
    email: str,
    _: bool = Depends(RoleCheck(allowed_permission=["user:all", "admin:all"])),
):
    user = User.get_user(email=email)
    show_my_record = Record.show_user_record(user.id)

    if show_my_record:
        return show_my_record


@app.post("/user/login", tags=["User"])
async def login(user_login: LoginModel):
    user = (
        session.query(User)
        .filter_by(email=user_login.email, password=user_login.password)
        .first()
    )
    if user:
        token = Auth.generate_user_token(email=user_login.email)
        return token

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ConstantMessage.INVALID_CREDENTIALS,
        )


@app.post("/user/refresh", tags=["User"])
async def refresh_token(refresh: RefreshToken):
    valid_token = Auth.decode_refresh_token(refresh.refresh_token)
    if valid_token:
        return Auth.generate_user_token(valid_token["email"])
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ConstantMessage.INVALID_CREDENTIALS,
        )

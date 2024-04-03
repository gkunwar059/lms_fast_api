from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    MetaData,
    DateTime,
    func,
    Table,
    Column,
    ARRAY,
    Select,
)
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import (
    relationship,
    Mapped,
    joinedload,
    mapped_column,
    DeclarativeBase,
)
from sqlalchemy.orm.exc import NoResultFound
from passlib.context import CryptContext

from sqlalchemy.exc import IntegrityError
from utils.constant_message import ConstantMessage
from email_validator import validate_email, EmailNotValidError
import hashlib
from auth.jwt_bearer import User_JwtBearer
from auth.jwt_handler import Auth
from fastapi import Depends
from database.db_connection import DATABASE_CONNECTION, Session, session, sessionmaker


class Base(DeclarativeBase):
    pass


class UserBook(Base):
    __tablename__ = "user_book"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))


class UserMagazine(Base):
    __tablename__ = "user_magazine"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    magazine_id: Mapped[int] = mapped_column(ForeignKey("magazines.id"))


# Association table for many to many relationship between User and Role
class UserRole(Base):
    __tablename__ = "user_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))


# Association table for many-to many realtionship between Role and Permission
class RolePermission(Base):
    __tablename__ = "role_permission"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    contact_no: Mapped[int] = mapped_column(nullable=False, unique=True)

    enroll_date: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.utcnow().date()
    )
    expiry_date: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.utcnow().date() + timedelta(days=60)
    )
    books = relationship("Book", secondary="user_book", back_populates="users")
    magazines = relationship(
        "Magazine", secondary="user_magazine", back_populates="users"
    )
    roles = relationship("Role", secondary="user_role", back_populates="users")

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verifying_password(password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)

    def __init__(self, name, email, password, address, contact_no, role_id):
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.contact_no = contact_no
        self.role_id = role_id

    @classmethod
    def get_user(cls, email):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_all_users(cls):
        return session.query(cls).all()

    @staticmethod
    def add_user(name, email, password, address, contact_no, role_id=None):
        hashed_password = User.get_hashed_password(password)

        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError(ConstantMessage.INVALID_EMAIL)

        if not (name and email and password and address and contact_no and role_id):
            raise ValueError(ConstantMessage.ALL_FIELD_REQUIRED)

        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            raise ValueError(ConstantMessage.ALREADY_EXIST_EMAIL)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            address=address,
            contact_no=contact_no,
            role_id=role_id,
        )
        session.add(new_user)
        try:
            session.commit()
            return ConstantMessage.USER_ADDED

        except IntegrityError as e:
            session.rollback()
            raise e

    @staticmethod
    def get_current_user(token: str = Depends(User_JwtBearer())):
        """Decode the token and fetch user details (email) and roles from the database."""
        user_email = Auth.decode_access_token(token)
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        # Fetch the user
        new_user = session.query(User).filter_by(email=user_email["email"]).first()
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        # Fetch roles and permissions for the user
        total_permission = []
        user_roles = session.query(UserRole).filter_by(user_id=new_user.id).all()
        for user_role in user_roles:
            role_permissions = session.query(RolePermission).filter_by(role_id=user_role.role_id).all()
            for role_permission in role_permissions:
                permission = session.query(Permission).filter_by(id=role_permission.permission_id).first()
                if permission:
                    total_permission.append(permission.name)

        return {
            "email": new_user.email,
            "role": total_permission,
        }




class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    users = relationship("User", secondary="user_role", back_populates="roles")
    permissions = relationship(
        "Permission", secondary="role_permission", back_populates="roles"
    )

    @staticmethod
    def create_role(name):
        role = Role(name=name)
        session.add(role)       #TODO:validation and exception are required later on 
        session.commit()
        return {"Role added sucessfully !"}

    @staticmethod
    def assign_role_to_user(role_id, user_id):
        user = session.query(User).get(user_id)
        role = session.query(Role).get(role_id)
        # role=session.query(Role).filter_by(id=role_id).first()  s #this approach and above get approach is similar working mechanism where the get is more consise and eazy to acess the

        if user and role:
            user.roles.append(role)
            session.commit()
            return True
        else:
            return False
        
    @staticmethod
    def get_permission(role_id):
        return session.scalars(
            Select(Role.name).where(Role.id == role_id)
        ).first()

class Permission(Base):
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    roles = relationship(
        "Role", secondary="role_permission", back_populates="permissions"
    )

    @staticmethod
    def create_permission(name):
        permission = Permission(name=name)
        session.add(permission)
        session.commit()
        return permission

    @staticmethod
    def assign_permission_to_role(permission_id, role_id):
        permission = session.query(Permission).get(permission_id)
        role = session.query(Role).get(role_id)

        if role and permission:
            role.permissions.append(
                permission
            )  # NOTE:role ma vayeko permission ma chai permission add garnu ho (yo permissions ma chai relationship le gard chai hunxa )-important concept nai ho , easy but needed many places
            session.commit()
            return True
        else:
            return False




class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[int] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    users = relationship("User", secondary="user_book", back_populates="books")
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"))
    publishers = relationship("Publisher", back_populates="books")
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    categories = relationship("Category", back_populates="books")
    records = relationship("Record", backref="books")

    def __init__(self, isbn, title, author, price, publisher_id=None, category_id=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        self.publisher_id = publisher_id
        self.category_id = category_id

    @staticmethod
    def get_book(isbn):
        book = session.query(Book).filter_by(isbn=isbn).first()
        return book

    @classmethod
    def get_all_books(cls):
        return session.query(cls).all()

    @staticmethod
    def add_book(isbn, title, author, price, publisher_id=None, category_id=None):

        if not (isbn and title and author and price and publisher_id and category_id):
            raise ValueError(ConstantMessage.ALL_FIELD_REQUIRED)

        existing_book = session.query(Book).filter_by(isbn=isbn).first()

        if existing_book:
            raise ValueError(ConstantMessage.BOOK_ALREADY_EXIT_OF_ISBN)

        book = Book(
            isbn=isbn,
            title=title,
            author=author,
            price=price,
            publisher_id=publisher_id,
            category_id=category_id,
        )
        session.add(book)
        try:
            session.commit()
            return ConstantMessage.BOOK_ADDED

        except IntegrityError as e:
            session.rollback()
            print(str(e))

    def borrow_book(self, user_id):
        try:

            book = session.query(Book).filter_by(isbn=self.isbn).first()
            user = session.query(User).filter_by(id=user_id).first()

            if not (book and user):
                raise NoResultFound(ConstantMessage.BOOK_OR_USER_NOT_FOUND)

            existing_record = (
                session.query(Record)
                .filter(
                    Record.user_id == user_id,
                    Record.returned == False,
                    Record.book_id == book.isbn,
                )
                .first()
            )

            if existing_record:
                return f"Already borrowed !"

            book.users.append(user)
            session.commit()

            record = Record(user_id=user_id, book_id=self.isbn, returned=False)
            session.add(record)
            session.commit()
            return ConstantMessage.RECORD_ADDED

        except Exception as e:
            print(e)
            session.rollback()

    def return_book(self, user_id):
        try:
            book = session.query(Book).filter_by(isbn=self.isbn).first()
            user = session.query(User).filter_by(id=user_id).first()

            if book is None and user is None:
                raise NoResultFound(ConstantMessage.PROVIDE_BOOK_USER)
            book.users.remove(user)
            session.commit()
            print(f"{user.name} has return  {book.title}")

            record = (
                session.query(Record)
                .filter_by(user_id=user_id, book_id=self.isbn, returned=False)
                .first()
            )
            if record:
                record.returned = True
                record.return_date = datetime.utcnow().date()
                session.commit()
                return ConstantMessage.UPDATE_RETURN_BOOK

        except NoResultFound as e:
            print(e)
            session.rollback()

        except Exception as e:
            print(e)
            session.rollback()


class Magazine(Base):
    __tablename__ = "magazines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    issn: Mapped[int] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    editor: Mapped[str] = mapped_column(nullable=False)
    users = relationship("User", secondary="user_magazine", back_populates="magazines")
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"))
    publishers = relationship("Publisher", back_populates="magazines")
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    categories = relationship("Category", back_populates="magazines")
    records = relationship("Record", backref="magazines")

    def __init__(self, issn, title, price, editor, publisher_id=None, category_id=None):
        self.issn = issn
        self.title = title
        self.price = price
        self.editor = editor
        self.publisher_id = publisher_id
        self.category_id = category_id

    @staticmethod
    def get_magazine(issn):
        return session.query(Magazine).filter_by(issn=issn).first()

    @staticmethod
    def add_magazine(issn, title, price, editor, publisher_id=None, category_id=None):

        if not (issn and title and price and editor and publisher_id and category_id):
            raise ValueError(ConstantMessage.ALL_FIELD_REQUIRED)

        existing_magazine = session.query(Magazine).filter_by(issn=issn).first()
        if existing_magazine:
            raise ValueError(ConstantMessage.MAGAZINE_ALREADY_EXIST)

        magazine = Magazine(
            issn=issn,
            title=title,
            price=price,
            editor=editor,
            publisher_id=publisher_id,
            category_id=category_id,
        )
        session.add(magazine)
        try:
            session.commit()
            return ConstantMessage.MAGAZINE_ADDED
        except IntegrityError as e:
            session.rollback()
            print(str(e))

    @classmethod
    def show_all_magazines(cls):
        return session.query(cls).all()

    def borrow_magazine(self, user_id):
        try:
            magazine = session.query(Magazine).filter_by(issn=self.issn).first()
            user = session.query(User).filter_by(id=user_id).first()

            if not (magazine and user):
                raise NoResultFound(ConstantMessage.MAGAZINE_AND_USER_NOT_FOUND)

            existing_record = (
                session.query(Record)
                .filter(
                    Record.user_id == user_id,
                    Record.returned == False,
                    Record.magazine_id == magazine.issn,
                )
                .first()
            )

            if existing_record:
                return f"Detail:Already exist !"

                # raise HTTPException (status_code=404,detail=f"{USER.name} has already borrowed a copy of {magazine.title} with the same issn number  ")

            magazine.users.append(user)
            session.commit()
            print(f"{user.name } has borrowed {magazine.title}")

            record = Record(user_id=user_id, magazine_id=self.issn, returned=False)
            session.add(record)
            session.commit()
            # better to return the created record than the message
            return ConstantMessage.RECORD_ADDED

        except NoResultFound as e:
            print(e)

    def return_magazine(self, user_id):
        try:
            magazine = session.query(Magazine).filter_by(issn=self.issn).first()
            user = session.query(User).filter_by(id=user_id).first()

            if magazine is None and user is None:
                raise NoResultFound(ConstantMessage.PROVIDE_MAGAZINE_USER)
            magazine.users.remove(user)
            session.commit()
            record = (
                session.query(Record)
                .filter_by(user_id=user_id, magazine_id=self.issn, returned=False)
                .first()
            )
            if record:
                record.returned = True
                record.return_date = datetime.utcnow().date()
                try:
                    session.commit()
                    return ConstantMessage.UPDATE_RETURN_MAGAZINE

                except IntegrityError as e:
                    session.rollback()
                    print(str(e))

        except NoResultFound as e:
            print(str(e))
            session.rollback()

        except Exception as e:
            print(str(e))
            session.rollback()


class Publisher(Base):
    __tablename__ = "publishers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    contact_no: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    books = relationship("Book", back_populates="publishers")
    magazines = relationship("Magazine", back_populates="publishers")

    def __init__(self, name, contact_no, address):
        self.name = name
        self.contact_no = contact_no
        self.address = address

    @classmethod
    def show_all_publishers(cls):
        return session.query(cls).all()

    @staticmethod
    def add_publisher(name, contact_no, address):
        if not (name and contact_no and address):
            raise ValueError(ConstantMessage.ALL_FIELD_REQUIRED)

        existing_publisher = session.query(Publisher).filter_by(name=name).first()
        if existing_publisher:
            raise ValueError(ConstantMessage.ALREADY_EXIST_PUBLISHER)

        publisher = Publisher(name=name, contact_no=contact_no, address=address)
        session.add(publisher)
        try:
            session.commit()
            return ConstantMessage.PUBLISHER_ADDED

        except IntegrityError as e:
            session.rollback()
            print(str(e))

    @classmethod
    def get_publisher(cls, name):
        publisher = session.query(Publisher).filter_by(name=name).first()
        return cls(publisher.name, publisher.contact_no, publisher.address)


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    magazines = relationship("Magazine", back_populates="categories")
    books = relationship("Book", back_populates="categories")

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_category(cls, name):
        return session.query(Category).filter_by(name=name).first()

    @classmethod
    def show_all_categories(cls):
        return session.query(cls).all()

    @staticmethod
    def add_category(name):
        if not name:
            raise ValueError("Name required !")

        existing_category = session.query(Category).filter_by(name=name).first()
        if existing_category:
            raise ValueError(ConstantMessage.CATEGORY_EXIST)
        category = Category(name=name)

        session.add(category)
        try:
            session.commit()
            return ConstantMessage.CATEGORY_ADDED

        except IntegrityError as e:
            session.rollback()
            print(str(e))


# class Role(Base):
#     __tablename__ = "roles"s
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     role: Mapped[str] = mapped_column(String, nullable=False, default=1)
#     permission = mapped_column(ARRAY(String), nullable=False)
#     user = relationship("User", back_populates="roles")

    # @staticmethod
    # def get_permission(role_id):
    #     return session.scalars(
    #         Select(Role.permission).where(Role.id == role_id)
    #     ).first()


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.isbn"), nullable=True)
    magazine_id: Mapped[int] = mapped_column(
        ForeignKey("magazines.issn"), nullable=True
    )
    returned: Mapped[bool] = mapped_column(nullable=False, default=False)
    return_date: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.utcnow().date() + timedelta(days=15)
    )
    borrow_date: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.utcnow().date()
    )

    def __init__(self, user_id, book_id=None, magazine_id=None, returned=False):
        if not book_id and not magazine_id:
            raise Exception(ConstantMessage.BOOK_MAGAZINE_NOT_FOUND)
        self.user_id = user_id
        self.book_id = book_id
        self.magazine_id = magazine_id
        self.returned = returned

    @classmethod
    def show_all_records(cls, user_id):
        return session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def show_user_record(cls, user_id):
        return session.query(cls).filter_by(user_id=user_id, returned=False).all()

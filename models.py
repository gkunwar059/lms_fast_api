from sqlalchemy import String,Integer,ForeignKey,MetaData,create_engine,DateTime,func,engine,Table,Column
from datetime import datetime,timedelta
from sqlalchemy.orm import Session,relationship,sessionmaker,session,Mapped,mapped_column,DeclarativeBase
from sqlalchemy.orm.exc import NoResultFound
from email_validator import validate_email,EmailNotValidError
import hashlib
from decouple import config

DATABASE_CONNECTION=config('database_connection')

class Base(DeclarativeBase):
    pass

try:
    engine=create_engine(DATABASE_CONNECTION,echo=False)
    print("Connection Okay") 
    
except Exception as er:
    print(er)
    print("connction is not successful ")


with Session(engine) as session:
    Session=sessionmaker(bind=engine)
    session=Session()
    
class MemberBook(Base):
    __tablename__ = 'member_book'
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
    book_id:Mapped[int] = mapped_column(ForeignKey('books.id'))
    
    
class MemberMagazine(Base):
    __tablename__ = 'member_magazine'
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
    magazine_id:Mapped[int] = mapped_column(ForeignKey('magazines.id'))
    
    
class Member(Base):
    __tablename__ =  "members"
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=False)
    member_type:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str]=mapped_column(nullable=False,unique=True)
    password:Mapped[str]=mapped_column(nullable=False)
    address:Mapped[str] = mapped_column(nullable=False)
    contact_no:Mapped[int] = mapped_column(nullable=False,unique=True)
    enroll_date:Mapped[DateTime] = mapped_column( DateTime(),default=datetime.utcnow().date())
    expiry_date:Mapped[DateTime] = mapped_column(DateTime(),default=datetime.utcnow().date() +timedelta(days=60))
    books = relationship('Book',secondary = 'member_book' , back_populates = 'members')
    magazines = relationship('Magazine',secondary = 'member_magazine',back_populates = 'members')
    records = relationship('Record',backref='members')
    
    def __init__(self,name,member_type,email,password,address,contact_no):
        self.name = name
        self.member_type = member_type
        self.email = email
        self.password=password
        self.address = address
        self.contact_no = contact_no
    
    
    @classmethod
    def get_member(cls, email):
        return session.query(cls).filter_by(email = email).first()
        
    @classmethod
    def get_all_members(cls):
        return session.query(cls).all()
        
    @staticmethod
    def add_member(name,member_type,email,password,address,contact_no):
        
        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError("Invalid email ,Please provide a valid email !")
    
        if not (name and member_type and email and password  and address and contact_no):
            raise  ValueError("All field required !")
        
        existing_member = session.query(Member).filter_by(email=email).first()
        if existing_member:
            raise ValueError("Member with this email already exists !")
        
        new_member = Member(name,member_type,email,password,address,contact_no)
        session.add(new_member)
        try:
            session.commit()
            return ("Member added Successfully !")
        
        except Exception as e:    
            session.rollback()
            raise e
        
    
class Book(Base):
    __tablename__ = 'books'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    isbn:Mapped[int] = mapped_column(nullable=False,unique=True)
    title:Mapped[str] = mapped_column(nullable=False)
    author:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[int] = mapped_column(nullable=False)
    members = relationship('Member',secondary = 'member_book',back_populates = 'books')
    publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
    publishers = relationship('Publisher',back_populates = 'books')
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    categories = relationship('Category',back_populates = 'books')
    records = relationship('Record',backref='books')
    
    def __init__(self,isbn,title,author,price,publisher_id=None,category_id=None ):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        self.publisher_id = publisher_id
        self.category_id = category_id
        
        
    @classmethod
    def get_book(cls,isbn):
        book = session.query(Book).filter_by(isbn=isbn).first()
        return cls(book.isbn,book.title,book.price,book.author)
        
  
    @classmethod
    def get_all_books(cls):
        return session.query(cls).all()
    
    
    @staticmethod
    def add_book(isbn,title,author,price,publisher_id=None,category_id=None):
        
        if not(isbn and title and author and price and publisher_id and category_id):
            raise ValueError("All field required !")
        
        existing_book=session.query(Book).filter_by(isbn=isbn).first()
        
        if existing_book:
            raise ValueError("Book is already exist with isbn numnber !")
        
        book = Book(isbn=isbn,title=title,author=author,price=price,publisher_id=publisher_id,category_id=category_id)
        session.add(book)
        try:
            session.commit()
            return("Book added Sucessfully  !")
        
        except Exception as e:
            session.rollback()
            print(str(e))
            
       
    def borrow_book(self,member_id):
        try:
            
            book = session.query(Book).filter_by(isbn=self.isbn).first()
            member = session.query(Member).filter_by(id=member_id).first()
            
            # if book is None and member is None:
            if not (book and member):
                raise NoResultFound("Both member and book not found  !")
            
            existing_record=session.query(Record).\
                filter(Record.member_id == member_id,Record.returned == False, Record.book_id == book.isbn) .\
                join(Book,Record.book_id == Book.id) .\
                filter(Book.isbn == book.isbn).first()  
                

            if existing_record:
                raise Exception (f"{member.name} has already borrowed a copy of {book.title} with the same ISBN number  ")
            
            book.members.append(member)
            session.commit()
            print(f"{member.name} has borrowed {book.title}")
            record = Record(member_id=member_id,book_id=self.isbn,returned=False)
            session.add(record)
            session.commit()
            return("Record add sucessfully !")
            
        except NoResultFound as e:
            print(e)
            session.rollback()
            
        except Exception as e:
            print(f"An Error occured :{e}")
            session.rollback()

    def return_book(self,member_id):
        try:
            book = session.query(Book).filter_by(isbn=self.isbn).first()
            member = session.query(Member).filter_by(id=member_id).first()

            if book is None and member is None:
                raise NoResultFound("provide both book and magazine")
            book.members.remove(member)
            session.commit()
            print(f"{member.name} has return  {book.title}")

            record = session.query(Record).filter_by(member_id=member_id,book_id=self.isbn,returned=False).first()
            if record:
                record.returned = True
                record.return_date = datetime.utcnow().date()
                session.commit()
                return("Update returned book sucessfully !")

        except NoResultFound as e:
            print(e)
            session.rollback()

        except Exception as e:
            print("Book and Member not found !")
            print(e)
            session.rollback()

class Magazine(Base):
    __tablename__ = 'magazines'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    issn:Mapped[int] = mapped_column(nullable=False,unique=True)
    title:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[int] = mapped_column(nullable=False)
    editor:Mapped[str] = mapped_column(nullable=False)
    members=relationship('Member',secondary = 'member_magazine',back_populates = 'magazines')    
    publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
    publishers = relationship('Publisher',back_populates = 'magazines')
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    categories = relationship('Category',back_populates = 'magazines')
    records = relationship('Record',backref='magazines')
    
    
    def __init__(self,issn,title,price,editor,publisher_id=None,category_id=None):
        self.issn = issn
        self.title = title
        self.price = price
        self.editor = editor
        self.publisher_id = publisher_id
        self.category_id = category_id
        
    
    @classmethod
    def get_magazine(cls,issn):
        magazine = session.query(Magazine).filter_by(issn=issn).first()
        return cls(magazine.issn,magazine.title,magazine.price,magazine.editor)
       
    
    @staticmethod
    def add_magazine(issn,title,price,editor,publisher_id=None,category_id=None):
        
        if not (issn and title and price and editor and publisher_id and category_id):
            raise ValueError("All field required !")
        
        existing_magazine=session.query(Magazine).filter_by(issn=issn).first()
        if existing_magazine:
            raise ValueError("Magazine already exists")
        
        magazine = Magazine(issn=issn,title=title,price=price,editor=editor,publisher_id=publisher_id,category_id=category_id)
        session.add(magazine)
        try:
            session.commit()
            return("Magazine added SucessFully !")
        except Exception as e:
            session.rollback()
            print(str(e))
            
            
            
    @classmethod
    def show_all_magazines(cls):
        return session.query(cls).all()
    
                  
    def borrow_magazine(self,member_id):
        try:
            magazine = session.query(Magazine).filter_by(issn=self.issn).first()
            member = session.query(Member).filter_by(id=member_id).first()

            if not(magazine and member):
                raise NoResultFound("Both member and book not found  !")
                
                
            existing_record=session.query(Record).\
                filter(Record.member_id == member_id,Record.returned == False) .\
                join(Magazine, Record.magazine_id == Magazine.id) .\
                filter(Magazine.issn == magazine.issn).first()
                
            if existing_record:
                    raise Exception (f"{member.name} has already borrowed a copy of {magazine.title} with the same issn number  ")
                
            
            magazine.members.append(member)
            session.commit()
            print(f"{member.name } has borrowed {magazine.title}")
            # create database for magazine 
            
            record=Record(member_id=member_id,magazine_id=self.issn,returned=False)
            session.add(record)
            try:
                session.commit()
                # print("Record add Sucessfully ")
                return("Record add Sucessfully ")
                
            except Exception as e:
                session.rollback()
                print(str(e))
        
        except NoResultFound as e:
            print(e)
            
        except Exception as e:
            print(f"No Magazine is found ")
            session.rollback()
            


    def return_magazine(self,member_id):
        try:
            magazine = session.query(Magazine).filter_by(issn=self.issn).first()
            member = session.query(Member).filter_by(id=member_id).first()
            
            if magazine is None and member is None:
                raise NoResultFound("Provide both magazine and member ")
            magazine.members.remove(member)
            session.commit()
            print(f"{member.name} has returned {magazine.title}")
            record = session.query(Record).filter_by(member_id=member_id,magazine_id=self.issn,returned=False).first()
            if record: 
                record.returned = True
                record.return_date = datetime.utcnow().date() 
                try:
                    session.commit()
                    # print("updated returned magazine sucessfully ! ")
                    return("updated returned magazine sucessfully ! ")
                    
                except Exception as e:
                    session.rollback()
                    print(str(e))    
                    
        except NoResultFound as e:
            print(str(e))  
            session.rollback()
                 
        except Exception as e:
            session.rollback()
            print(str(e))            
    
    
    
class Publisher(Base):
    __tablename__ = 'publishers'
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True,nullable=False)
    contact_no:Mapped[str] = mapped_column(String(20),nullable=False)
    address:Mapped[str] = mapped_column(nullable=False)
    books = relationship('Book',back_populates = 'publishers')
    magazines = relationship('Magazine',back_populates = 'publishers')
    
    def __init__(self,name,contact_no,address):
        self.name = name
        self.contact_no = contact_no
        self.address = address
        
    @classmethod
    def show_all_publishers(cls):
        return session.query(cls).all()
    
    
    @staticmethod
    def add_publisher(name,contact_no,address):
        if not(name and contact_no and address):
            raise ValueError("All field required !")
        
        existing_publisher=session.query(Publisher).filter_by(name=name).first()
        if existing_publisher:
            raise ValueError("Already publisher exists")
        
        publisher=Publisher(name=name,contact_no=contact_no,address=address)
        session.add(publisher)
        try:
            session.commit()
            return("Publisher added Sucessfully !")
        
        except Exception as e:
            session.rollback()
            print(str(e))
            
            
                  
    @classmethod
    def get_publisher(cls,name):
        publisher=session.query(Publisher).filter_by(name=name).first()
        return cls(publisher.name,publisher.contact_no,publisher.address)
    
    
class Category(Base):
    __tablename__ = 'category'
    
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True,nullable=False)
    magazines = relationship('Magazine',back_populates='categories')
    books = relationship('Book',back_populates='categories')

    
    def __init__(self,name):
        self.name=name
    
    @classmethod
    def get_category(cls,name):
        category=session.query(Category).filter_by(name=name).first()
        return cls(category.name)
    
    @classmethod
    def show_all_categories(cls):
        return session.query(cls).all()
    
    
    @staticmethod
    def add_category(name):
        if not name:
            raise ValueError("Name required !")
        
        existing_category=session.query(Category).filter_by(name=name).first()
        if existing_category:
            raise ValueError("Category already exists")
        category=Category(name=name)
        
        
        session.add(category)
        try:
            session.commit()
            return("Category Added SucessFully !")
        
        except Exception as e:
            session.rollback()
            print(str(e))    
   

    
class Librarian(Base):
    __tablename__='librarians'
    
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str]=mapped_column(nullable=False,unique=True)
    email:Mapped[str]=mapped_column(nullable=False,unique=True)
    password:Mapped[str]=mapped_column(nullable=False)
    contact_no:Mapped[int]=mapped_column(nullable=False)
       
    def __init__(self,name,contact_no,email,password):
        self.name=name
        self.contact_no=contact_no
        self.email=email
        self.password=password
    
   
    @classmethod
    def get_librarian_by_email(cls, email):
        return session.query(cls).where(Librarian.email==email).first()
       
    
class Record(Base):
    __tablename__ = 'records'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
    book_id:Mapped[int] = mapped_column(ForeignKey('books.isbn'),nullable=True)
    magazine_id:Mapped[int] = mapped_column(ForeignKey('magazines.issn'),nullable=True)
    returned:Mapped[bool]=mapped_column(nullable=False,default=False)
    return_date:Mapped[DateTime] = mapped_column(DateTime(),default=datetime.utcnow().date() +timedelta(days=15))
    borrow_date:Mapped[DateTime] = mapped_column(DateTime(),default = datetime.utcnow().date())
    
    
    def __init__(self,member_id,book_id=None,magazine_id=None,returned=False):
        
        if not book_id and not magazine_id:
            raise Exception("No book and Magazine Found  !")
        self.member_id=member_id
        self.book_id=book_id
        self.magazine_id=magazine_id
        self.returned=returned
        
    @classmethod   
    def show_all_records(cls, member_id):
        return session.query(cls).filter_by(member_id=member_id).all()
    
    
    @classmethod
    def show_user_record(cls, member_id):
        return session.query(cls).filter_by(member_id=member_id,returned=False).all()
    
    
    
    
    
  
from sqlalchemy import String,Integer,ForeignKey,MetaData,create_engine,DateTime,func,engine,Table,Column
from datetime import datetime,timedelta
from sqlalchemy.orm import Session,relationship,sessionmaker,session,Mapped,mapped_column,DeclarativeBase
from sqlalchemy.orm.exc import NoResultFound
class Base(DeclarativeBase):
    pass

try:
    # engine=create_engine('postgresql://postgres:123456789@127.0.0.1:5432/postgres',echo=False)
    engine=create_engine('postgresql://postgres:postgres@127.0.0.1:5432/postgres',echo=False)
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
    address:Mapped[str] = mapped_column(nullable=False)
    contact_no:Mapped[str] = mapped_column(String(20),nullable=False,unique=True)
    enroll_date:Mapped[DateTime] = mapped_column( DateTime(),default=datetime.utcnow().date())
    expiry_date:Mapped[DateTime] = mapped_column(DateTime(),default=datetime.utcnow().date() +timedelta(days=60))
    books = relationship('Book',secondary = 'member_book' , back_populates = 'members')
    magazines = relationship('Magazine',secondary = 'member_magazine',back_populates = 'members')
    records = relationship('Record',backref='members')
    
    def __init__(self,name,member_type,email,address,contact_no):
        self.name = name
        self.member_type = member_type
        self.email = email
        self.address = address
        self.contact_no = contact_no
    
     
    @classmethod
    def get_member(cls, email):
        return session.query(cls).filter_by(email = email).first()
        
    @classmethod
    def get_all_members(cls):
        return session.query(cls).all()
        
    @staticmethod
    def add_member(name,member_type,email,address,contact_no):
    
        if not name:
            print("name cannot be empty ")
            return
        elif not member_type :
            print('member_type cannot be empty !')
            return
        elif not email:
            print("email connot be empty !")
            return
        elif not address:
            print("address cannot be empty !")
            return
        elif not contact_no:
            print("contact_no cannot be none !")
            return
        
        member = Member(name,member_type,email,address,contact_no)
        session.add(member)
        session.commit()
        print("Member added Successfully !")
        
     
        
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
    def get_all_books(cls):
        return session.query(cls).all()
    
    @staticmethod
    def add_book(isbn,title,author,price,publisher_id=None,category_id=None):
        book = Book(isbn=isbn,title=title,author=author,price=price,publisher_id=publisher_id,category_id=category_id)
        session.add(book)
        session.commit()
        print("Book added SucessFull !")
       
       
    def borrow_book(self,member_id):
        try:
            
            book = session.query(Book).filter_by(id=self.id).first()
            member = session.query(Member).filter_by(id=member_id).first()
            
            if book is None and member is None:
                raise NoResultFound("Both member and book not found  !")
            
            existing_record=session.query(Record).\
                filter(Record.member_id == member_id,Record.returned == False) .\
                join(Book,Record.book_id == Book.id) .\
                filter(Book.isbn == book.isbn).first()  
                
                
            if existing_record:
                raise Exception (f"{member.name} has already borrowed a copy of {book.title} with the same ISBN number  ")
            
            book.members.append(member)
            session.commit()
            print(f"{member.name} has borrowed {book.title}")
            record = Record(member_id=member_id,book_id=self.id,returned=False)
            session.add(record)
            session.commit()
            print("Record add sucessfully !")
            
        except NoResultFound as e:
            print(e)
            
        except Exception as e:
            print(f"An Error occured :{e}")


    def return_book(self,member_id):
        try:
            book = session.query(Book).filter_by(id=self.id).first()
            member = session.query(Member).filter_by(id=member_id).first()

            if book is None and member is None:
                raise NoResultFound("provide both book and magazine")
            book.members.remove(member)
            session.commit()
            print(f"{member.name} has return  {book.title}")

            record = session.query(Record).filter_by(member_id=member_id,book_id=self.id,returned=False).first()
            if record:
                record.returned = True
                record.return_date = datetime.utcnow().date()
                session.commit()
                print("Update returned book sucessfully !")

        except NoResultFound as e:
            print(e)

        except Exception as e:
            print("Book and Member not found !")
            print(e)

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
        magazine = Magazine(issn=issn,title=title,price=price,editor=editor,publisher_id=publisher_id,category_id=category_id)
        session.add(magazine)
        session.commit()
        print("Magazine added SucessFully !")
        
    @classmethod
    def show_all_magazines(cls):
        return session.query(cls).all()
    
            
            
    def borrow_magazine(self,member_id):
        try:
            magazine = session.query(Magazine).filter_by(id=self.id).first()
            member = session.query(Member).filter_by(id=member_id).first()

            if magazine is None and member is None:
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
            record=Record(member_id=member_id,magazine_id=self.id,returned=False)
            session.add(record)
            session.commit()
            print("Record add Sucessfully ")
            
        
        except NoResultFound as e:
            print(e)
            
        except Exception as e:
            print(f"No Magazine is found ")
            

    def return_magazine(self,member_id):
        try:
            magazine = session.query(Magazine).filter_by(id=self.id).first()
            member = session.query(Member).filter_by(id=member_id).first()
            
            if magazine is None and member is None:
                raise NoResultFound("Provide both magazine and member ")
            magazine.members.remove(member)
            session.commit()
            print(f"{member.name} has returned {magazine.title}")
            record = session.query(Record).filter_by(member_id=member_id,magazine_id=self.id,returned=False).first()
            if record: 
                record.returned = True
                record.return_date = datetime.utcnow().date() 
                session.commit()
                print("updated returned magazine sucessfully ! ")
                    
        except NoResultFound as e:
            print(e)       
        except Exception as e:
            print("Magazine and Member is not found !")
    
    
            
    
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
        publisher=Publisher(name=name,contact_no=contact_no,address=address)
        session.add(publisher)
        session.commit()
        print("Publisher added Sucessfully !")
    
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
        category=Category(name=name)
        session.add(category)
        session.commit()
        print("Category Added SucessFully !")
        
   

    
class Librarian(Base):
    __tablename__='librarians'
    
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str]=mapped_column(nullable=False,unique=True)
    email:Mapped[str]=mapped_column(nullable=False,unique=True)
    contact_no:Mapped[int]=mapped_column(nullable=False)
       
    def __init__(self,name,contact_no,email):
        self.name=name
        self.contact_no=contact_no
        self.email=email
      
        
    @classmethod
    def get_librarian_by_email(cls, email):
        return session.query(cls).filter_by(email=email).one_or_none()
       
    
class Record(Base):
    __tablename__ = 'records'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
    book_id:Mapped[int] = mapped_column(ForeignKey('books.id'),nullable=True)
    magazine_id:Mapped[int] = mapped_column(ForeignKey('magazines.id'),nullable=True)
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
    
  
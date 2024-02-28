from sqlalchemy import String,Integer,ForeignKey,MetaData,create_engine,DateTime,func,engine,Table,Column
from datetime import datetime,timedelta
from sqlalchemy.orm import Session,relationship,sessionmaker,session,Mapped,mapped_column,DeclarativeBase

class Base(DeclarativeBase):
    pass

try:
    engine=create_engine('postgresql://postgres:123456789@127.0.0.1:5432/postgres',echo=False)
    print("Connection Okey") 
    
except Exception as er:
    print(er)
    print("connction is not successful ")


with Session(engine) as session:
    Session=sessionmaker(bind=engine)
    session=Session()
    
# association table of member and books
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
    
    
class Members(Base):
    __tablename__ =  "members"
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=False)
    member_type:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str]=mapped_column(nullable=False,unique=True)
    address:Mapped[str] = mapped_column(nullable=False)
    contact_no:Mapped[str] = mapped_column(String(20),nullable=False,unique=True)
    enroll_date:Mapped[DateTime] = mapped_column( DateTime(),default=datetime.utcnow().date())
    expiry_date:Mapped[DateTime] = mapped_column(DateTime(),default=datetime.utcnow().date() +timedelta(days=60))
    
    # testing librarian --- other working fine 
    # librarian_id:Mapped[Integer]=mapped_column(ForeignKey('librarians.id'))
    
    books = relationship('Books',secondary = 'member_book' , back_populates = 'members')
    magazines = relationship('Magazine',secondary = 'member_magazine',back_populates = 'members')
    records = relationship('Records',backref='members')
    # librarian 
    
    def __init__(self,name,member_type,email,address,contact_no):
        self.name=name
        self.member_type=member_type
        self.email=email
        self.address=address
        self.contact_no=contact_no
        
    
    # need revision this concept
    @classmethod 
    def get_member(cls,email):
        member= session.query(Members).filter_by(email=email).first()
        return cls(member.name,member.member_type,member.email,member.address,member.contact_no)
        
    
    def get_all_members(self):
        return session.query(Members).all()
        
    
    def add_member(name,member_type,email,address,contact_no):
        member=Members(name,member_type,email,address,contact_no)
        session.add(member)
        session.commit()
        
    def delete_member(self):
        member=session.query(Members).filter_by(email=self.email).delete()
        session.commit()
        
    def update_member(self,name=None,member_type=None,email=None,address=None,contact_no=None):
        member=session.query(Members).filter_by(email=self.email).first()
        
        if member:
            if name:
                member.name=name
                
            if member_type:
                member.member_type=member_type
            
            if email:
                member.email=email
                
            if address:
                member.address=address
                
            if contact_no:
                member.contact_no=contact_no
            
            session.commit()
            
        else:
            print("Member not found !")
            
        
    # borrow_book   
    def borrow_book(member_id,book_id):
        book=session.query(Books).filter_by(id=book_id).first()
        member=session.query(Members).filter_by(id=member_id).first()
        
        if book and member:
            book.members.append(member)
            session.commit()
            print(f"{member.name} has borrowed {book.title}")
            
            # create a record for borrow book 
            record=Records(member_id=member_id,book_id=book_id,returned=False)
            session.add(record)
            session.commit()
            print("Record add sucessfully !")
        else:
            print("Book not found !")        
        
    # return book 
    # validation required 
    # if three book is taken by one person then it is difficult to delete 
    # exception handling is required 
    def return_book(member_id,book_id):
        book=session.query(Books).filter_by(id=book_id).first()
        member=session.query(Members).filter_by(id=member_id).first()
        
        if book and member:
            book.members.remove(member)
            session.commit()
            print(f"{member.name} has return  {book.title}")
        #    find the already existing records
            record=session.query(Records).filter_by(member_id=member_id,book_id=book_id,returned=False).first()
            # update record
            if record:
                record.returned=True
                record.return_date=datetime.utcnow().date()
                session.commit()
                print("Update returned book sucessfully !")
            else:
                print("Record not found !")
        else:
            print("Book and Member not found !")
            
        
        
        # borrow_magazine
    def borrow_magazine(member_id,magazine_id):
        magazine=session.query(Magazine).filter_by(id=magazine_id).first()
        member=session.query(Members).filter_by(id=member_id).first()

        if magazine and member:
            magazine.members.append(member)
            session.commit()
            print(f"{member.name } has borrowed {magazine.title}")
            # create database for magazine 
            record=Records(member_id=member_id,magazine_id=magazine_id,returned=False)
            session.add(record)
            session.commit()
            print("Record add Sucessfully ")
        else:
            print("Magazine and Member is not Found !")   
            
            
            #return magazine  
            # exception handling 
            # validation 
            
    def return_magazine(member_id,magazine_id):
        magazine=session.query(Magazine).filter_by(id=magazine_id).first()
        member=session.query(Members).filter_by(id=member_id).first()
        
        if magazine and member:
            magazine.members.remove(member)
            session.commit()
            print(f"{member.name} has returned {magazine.title}")
            # find existing magazine here 
            record=session.query(Records).filter_by(member_id=member_id,magazine_id=magazine_id,returned=False).first()
            if record: #record bheteu bhane chai tala ko kura change garnu hai ta
                record.returned=True
                record.return_date=datetime.utcnow().date() #aajha ko date ma book return garyo date change vayo haina ta 
                session.commit()
                print("updated returned magazine sucessfully ! ")
                
            
        else:
            print("Magazine and Member is not found !")
            
    
class Books(Base):
    __tablename__ = 'books'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    isbn:Mapped[int] = mapped_column(nullable=False,unique=True)
    title:Mapped[str] = mapped_column(nullable=False)
    author:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[int] = mapped_column(nullable=False)
    # is_available:Mapped[bool]=mapped_column(nullable=False)
    
    members = relationship('Members',secondary = 'member_book',back_populates = 'books')
    publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
    publishers = relationship('Publisher',back_populates = 'books')
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    categories = relationship('Category',back_populates = 'books')
    # testing librarians
    # librarian_id:Mapped[Integer]=mapped_column(ForeignKey('librarians.id'))
    records = relationship('Records',backref='books')
    
    def __init__(self,isbn,title,author,price):
        self.isbn=isbn
        self.title=title
        self.author=author
        self.price=price
        # self.is_available=True
    
    
    @classmethod
    def get_book(cls,isbn):
        book=session.query(Books).filter_by(isbn=isbn).first()
        return cls(book.isbn,book.title,book.author,book.price)
    
    # @staticmethod    
    def show_all_book(self):
        return session.query(Books).all()
    
    
    def delete_book(self):
        book=session.query(Books).filter_by(isbn=self.isbn).delete()
        session.commit()
        
    def update_book(self,isbn=None,title=None,author=None,price=None):
        book=session.query(Books).filter_by(isbn=self.isbn).first()
        if book:
            if isbn:
                book.isbn=isbn
            if title:
                book.title=title
            if author:
                book.author=author
            if price:
                book.price=price
            session.commit()
        
        else:
            print("Book not Found !!")
            
        
class Magazine(Base):
    __tablename__ = 'magazines'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    issn:Mapped[int] = mapped_column(nullable=False,unique=True)
    title:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[int] = mapped_column(nullable=False)
    editor:Mapped[str] = mapped_column(nullable=False)
    # is_available:Mapped[bool]=mapped_column(nullable=False)
    members=relationship('Members',secondary = 'member_magazine',back_populates = 'magazines')    
    publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
    publishers = relationship('Publisher',back_populates = 'magazines')
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    categories = relationship('Category',back_populates = 'magazines')
    # testing the phase
    # librarian_id:Mapped[Integer]=mapped_column(ForeignKey('librarians.id'))
    
    records = relationship('Records',backref='magazines')
    
    
    
    def __init__(self,issn,title,price,editor):
        self.issn=issn
        self.title=title
        self.price=price
        self.editor=editor
        
    
    @classmethod
    def get_magazine(cls,issn):
        magazine=session.query(Magazine).filter_by(issn=issn).first()
        return cls(magazine.issn,magazine.title,magazine.price,magazine.editor)
       
    
    def show_all_magazine():
        return session.query(Magazine).all()
    
    def delete_magazine(self):
        magazine=session.query(Magazine).filter_by(issn=self.issn).delete()
        session.commit()
        
    def update_magazine(self,issn=None,title=None,price=None,editor=None):
        magazine=session.query(Magazine).filter_by(issn=self.issn).first()
        if magazine:
            if issn:
                magazine.issn=issn
                
            if title:
                magazine.title=title
                
            if price:
                magazine.price=price
                
            if editor:
                magazine.editor=editor
            session.commit()
        
        else:
            print("Magazine  not Found !!")
            
    
class Publisher(Base):
    __tablename__ = 'publishers'
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True,nullable=False)
    contact_no:Mapped[str] = mapped_column(String(20),nullable=False)
    address:Mapped[str] = mapped_column(nullable=False)
    books = relationship('Books',back_populates = 'publishers')
    magazines = relationship('Magazine',back_populates = 'publishers')
    # records = relationship('Records',backref='publishers')
    
    def __init__(self,name,contact_no,address):
        self.name=name
        self.contact_no=contact_no
        self.address=address
        
    
    def show_all_publisher():
        return session.query(Publisher).all()
    
    @classmethod
    def get_publisher(cls,name):
        publisher=session.query(Publisher).filter_by(name=name).first()
        return cls(publisher.name,publisher.contact_no,publisher.address)
    
    def delete_publisher(self):
        publisher=session.query(Publisher).filter_by(name=self.name).delete()
        session.commit()
        
        
    def update_publisher(self,name=None,contact_no=None,address=None):
        publisher=session.query(Publisher).filter_by(name=self.name).first()
        if publisher:
            if name:
                publisher.name=name
                
            if contact_no:
                publisher.contact_no=contact_no
                
            if address:
                publisher.address=address
                
        
            session.commit()
        
        else:
            print("Publisher  not Found !!")
    


class Category(Base):
    __tablename__ = 'category'
    
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True,nullable=False)
    magazines = relationship('Magazine',back_populates='categories')
    books = relationship('Books',back_populates='categories')
    # records = relationship('Records',backref='category')
    
    def __init__(self,name):
        self.name=name
    
    @classmethod
    def get_category(cls,name):
        category=session.query(Category).filter_by(name=name).first()
        return cls(category.name)
    
    def show_all_category():
        return session.query(Category).all()
     
    def delete_category(self):
        category=session.query(Category).filter_by(name=self.name).delete()
        session.commit()
    
    def update_category(self,name=None):
        category=session.query(Category).filter_by(name=self.name).first()
        if category:
            if name:
                category.name=name
                
           
            session.commit()
        
        else:
            print("Category   not Found !!")


    
class Librarian(Base):
    __tablename__='librarians'
    
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str]=mapped_column(nullable=False,unique=True)
    contact_no:Mapped[int]=mapped_column(nullable=False)
    # member=relationship('Members',backref='librarian')
    # book=relationship('Books',backref='librarian')  #librarian =>Librarian (class just a case sensative)
    # magazine=relationship('Magazine',backref='librarian')
    # record=relationship('Records',backref='librarian')
    
    # TODO -manage books -manage magazine - manage records
       
    def __init__(self,name,contact_no):
        self.name=name
        self.contact_no=contact_no
        
    
        
    
class Records(Base):
    __tablename__ = 'records'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
    book_id:Mapped[int] = mapped_column(ForeignKey('books.id'),nullable=True)
    magazine_id:Mapped[int] = mapped_column(ForeignKey('magazines.id'),nullable=True)
    returned:Mapped[bool]=mapped_column(nullable=False,default=False)
    return_date:Mapped[DateTime] = mapped_column(DateTime(),default=datetime.utcnow().date() +timedelta(days=15))
    borrow_date:Mapped[DateTime] = mapped_column(DateTime(),default = datetime.utcnow().date())
    
    # testing librarian data 
    # librarian_id:Mapped[Integer]=mapped_column(ForeignKey('librarians.id'))
    
    
    def __init__(self,member_id,book_id=None,magazine_id=None,returned=False):
        
        if not book_id and not magazine_id:
            raise Exception("No book and Magazine Found  !")
        self.member_id=member_id
        self.book_id=book_id
        self.magazine_id=magazine_id
        self.returned=returned
        
    @staticmethod
    def show_all_record():
        return session.query(Records).all()
    
  
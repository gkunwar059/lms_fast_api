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
    books = relationship('Books',secondary = 'member_book' , back_populates = 'members')
    magazines = relationship('Magazine',secondary = 'member_magazine',back_populates = 'members')
    records = relationship('Records',backref='members')
    
    def __init__(self,name,member_type,email,address,contact_no):
        self.name=name
        self.member_type=member_type
        self.email=email
        self.address=address
        self.contact_no=contact_no
        
    def get_member(id):
        member=session.query(Members).filter_by(id=id).first()
        return member
    
    def get_all_members():
        member=session.query(Members).all()
        print(member)
        return member
    
    def add_member(name,member_type,email,address,contact_no):
        member=Members(name,member_type,email,address,contact_no)
        session.add(member)
        session.commit()
        
    # def update_member(self,name=None,member_type=None,email=None,address=None,contact_no=None):
    #     member=session.query(Members).filter_by(id=id).first()

    #     if name:
    #         Members.name=name
    #     if member_type:
    #         Members.member_type=member_type
    #     if email:
    #         Members.email=email
            
    #     if address:
    #         Members.address=address
            
    #     if contact_no:
    #         Members.contact_no=contact_no
            
    #     session.commit()
    #     updated_member=Members.get_member(member.id)
    #     return updated_member
    
    # def delete_member(id):
    #     member=Members
    
class Books(Base):
    __tablename__ = 'books'
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    isbn:Mapped[int] = mapped_column(nullable=False)
    title:Mapped[str] = mapped_column(nullable=False,unique=True)
    author:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[int] = mapped_column(nullable=False)
    members = relationship('Members',secondary = 'member_book',back_populates = 'books')
    publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
    publishers = relationship('Publisher',back_populates = 'books')
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    categories = relationship('Category',back_populates = 'books')
    records = relationship('Records',backref='books')
    
    
       
class Magazine(Base):
    __tablename__ = 'magazines'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    issn:Mapped[int] = mapped_column(nullable=False,unique=True)
    title:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[int] = mapped_column(nullable=False)
    editor:Mapped[str] = mapped_column(nullable=False)
    members=relationship('Members',secondary = 'member_magazine',back_populates = 'magazines')    
    publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
    publishers = relationship('Publisher',back_populates = 'magazines')
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    categories = relationship('Category',back_populates = 'magazines')
    records = relationship('Records',backref='magazines')


class Publisher(Base):
    __tablename__ = 'publishers'
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True,nullable=False)
    contact_no:Mapped[str] = mapped_column(String(20),nullable=False)
    address:Mapped[str] = mapped_column(nullable=False)
    books = relationship('Books',back_populates = 'publishers')
    magazines = relationship('Magazine',back_populates = 'publishers')
    records = relationship('Records',backref='publishers')


class Category(Base):
    __tablename__ = 'category'
    
    id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True,nullable=False)
    magazines = relationship('Magazine',back_populates='categories')
    books = relationship('Books',back_populates='categories')
    records = relationship('Records',backref='category')
    
    
class Records(Base):
    __tablename__ = 'records'
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
    book_id:Mapped[int] = mapped_column(ForeignKey('books.id'))
    magazine_id:Mapped[int] = mapped_column(ForeignKey('magazines.id'))
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
    return_date:Mapped[DateTime] = mapped_column(DateTime(),nullable=True)
    borrow_date:Mapped[DateTime] = mapped_column(DateTime(),default = datetime.utcnow().date())
    
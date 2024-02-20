# from sqlalchemy import String,Integer,ForeignKey,MetaData,create_engine,DateTime,func,engine,Table,Column
# from datetime import datetime,timedelta
# from sqlalchemy.orm import Session,relationship,sessionmaker,session,Mapped,mapped_column,DeclarativeBase

# class Base(DeclarativeBase):
#     pass

# try:
#     engine=create_engine('postgresql://postgres:123456789@127.0.0.1:5432/postgres',echo=False)
#     print("Connection Okey") 
    
# except Exception as er:
#     print(er)
#     print("connction is not successful ")

# metadata=MetaData()

# with Session(engine) as session:
#     Session=sessionmaker(bind=engine)
#     session=Session() 


# class Members(Base):
#     __tablename__= "members"
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name:Mapped[str] = mapped_column(nullable=False)
#     member_type:Mapped[str] = mapped_column(nullable=False)
#     address:Mapped[str] = mapped_column(nullable=False)
#     contact_no:Mapped[int] = mapped_column(String(10),nullable=False)
#     enroll_date:Mapped[DateTime] = mapped_column( DateTime(),default=datetime.utcnow().date())
#     expiry_date:Mapped[DateTime] = mapped_column(DateTime(),default=datetime.utcnow().date() +timedelta(days=60))
#     books:Mapped[str]=relationship('Books',back_populates='member')

#     def __init__(self,name,member_type,address,contact_no):
#         # self.id=id
#         self.name = name
#         self.member_type = member_type
#         self.address = address
#         self.contact_no = contact_no
      
        
#     @staticmethod    
#     def get_member(id):
#         member=session.query(Members).filter_by(id=id).first()
#         return member
    
#     @staticmethod
#     def get_all_member():
#         member=session.query(Members).all()
#         return member
    
#     def add_member(name,member_type,address,contact_no):
#         member=Members(name=name,member_type=member_type,address=address,contact_no=contact_no)
#         session.add(member)
#         session.commit()
        
        
    
#     # def update_member():
#     #     pass
    
#     # def delete_member():
#     #     pass
    
    
# class Books(Base):
#     __tablename__='books'
    
#     isbn:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
#     title:Mapped[str]=mapped_column(nullable=False)
#     author:Mapped[str]=mapped_column(nullable=False)
#     price:Mapped[int]=mapped_column(nullable=False)
#     # foreign key
#     member_id:Mapped[int]=mapped_column(ForeignKey('members.id'),nullable=False)
#     member=relationship('Members',back_populates='books')
    
#     def __init__(self,isbn,title,author,price):
#         self.isbn=isbn
#         self.title=title
#         self.author=author
#         self.price=price
    
#     def get_book(id):
#         pass
    
#     def get_all_book():
#         pass
    
#     def add_book():
#         pass
    
#     def update_book():
#         pass
    
#     def delete_book():
#         pass
    
    
       
# class Magazine(Base):
#     __tablename__='magazine'
    
#     issn:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
#     title:Mapped[str]=mapped_column(nullable=False)
#     price:Mapped[int]=mapped_column(nullable=False)
#     editor:Mapped[str]=mapped_column(nullable=False)
    
    
#     def __init__(self,issn,title,price,editor):
#         self.issn=issn
#         self.title=title
#         self.price=price
#         self.editor=editor
        
        
#     def get_magazine(id):
#         pass
    
#     def get_all_magazine():
#         pass
    
#     def add_magazine():
#         pass
    
#     def update_magazine():
#         pass
    
#     def delete_magazine():
#         pass

    

# class Publisher(Base):
#     __tablename__='publisher'
    
#     id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
#     name:Mapped[str]=mapped_column(nullable=False)
#     contact_no:Mapped[int]=mapped_column(nullable=False)
#     address:Mapped[str]=mapped_column(nullable=False)
    
#     def __init__(self,id,name,contact_no,address):
#         self.id=id
#         self.name=name
#         self.contact_no=contact_no
#         self.address=address
        
#     def get_publisher(id):
#         pass
    
#     def get_all_publisher():
#         pass
    
#     def add_publisher():
#         pass
    
#     def update_publisher():
#         pass
    
#     def delete_publisher():
#         pass
    
    

# class Category(Base):
#     __tablename__='category'
    
#     id:Mapped[int]=mapped_column(primary_key=True , autoincrement=True)
#     name:Mapped[str]=mapped_column(nullable=False)
    
    
#     def __init__(self,id,name):
#         self.id=id
#         self.name=name
        
#     def get_category(id):
#         pass
    
#     def get_all_category():
#         pass
    
#     def add_category():
#         pass
    
#     def update_category():
#         pass
    
#     def delete_category():
#         pass
    
    
    

# class Librarian(Base):
#     __tablename__='librarian'
    
#     id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
#     name:Mapped[str]=mapped_column(nullable=False)
#     contact_no:Mapped[int]=mapped_column(nullable=False)
    
#     def __init__(self,id,name,contact_no):
#         self.id=id
#         self.name=name
#         self.contact_no=contact_no
        
#     def get_librarian(id):
#         pass
    
#     def get_all_librarian():
#         pass
    
#     def add_librarian():
#         pass
    
#     def update_librarian():
#         pass
    
#     def delete_librarian():
#         pass
    
    
    
# class Records(Base):
#     __tablename__='records'
    
#     id:Mapped[int]=mapped_column(primary_key=True,autoincrement=False)
#     member_id:Mapped[int]= ''
#     book_id:Mapped[int]=''
#     magazine_id:Mapped[int]=''
#     category_id:Mapped[int]=''
#     return_date:Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
#     borrow_date:Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    
    
    
#     def __init__(self,id,member_id,book_id,magazine_id,category_id,return_date,borrow_date):
#         self.id=id
#         self.member_id=member_id
#         self.book_id=book_id
#         self.magazine_id=magazine_id
#         self.category_id=category_id
#         self.return_date=return_date
#         self.borrow_date=borrow_date
        
        
#     def get_record(id):
#         pass
    
#     def get_all_record():
#         pass
    
#     def add_record():
#         pass
    
#     def update_record():
#         pass
    
#     def delete_record():
#         pass


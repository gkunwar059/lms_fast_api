# # --------------------------DATABASE--------------------------------------#
# from sqlalchemy import String,Integer,ForeignKey,MetaData,create_engine,DateTime,func,engine,Table,Column
# from datetime import datetime,timedelta
# from sqlalchemy.orm import Session,relationship,sessionmaker,session,Mapped,mapped_column,DeclarativeBase
# from sqlalchemy.orm.exc import NoResultFound
# class Base(DeclarativeBase):
#     pass

# try:
#     engine=create_engine('postgresql://postgres:123456789@127.0.0.1:5432/postgres',echo=False)
#     print("Connection Okey") 
    
# except Exception as er:
#     print(er)
#     print("connction is not successful ")


# with Session(engine) as session:
#     Session=sessionmaker(bind=engine)
#     session=Session()
    
# # association table of member and books
# class MemberBook(Base):
#     __tablename__ = 'member_book'
#     id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
#     member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
#     book_id:Mapped[int] = mapped_column(ForeignKey('books.id'))
    
    
# class MemberMagazine(Base):
#     __tablename__ = 'member_magazine'
#     id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
#     member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
#     magazine_id:Mapped[int] = mapped_column(ForeignKey('magazines.id'))
    
    
# class Member(Base):
#     __tablename__ =  "members"
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name:Mapped[str] = mapped_column(nullable=False)
#     member_type:Mapped[str] = mapped_column(nullable=False)
#     email:Mapped[str]=mapped_column(nullable=False,unique=True)
#     address:Mapped[str] = mapped_column(nullable=False)
#     contact_no:Mapped[str] = mapped_column(String(20),nullable=False,unique=True)
#     enroll_date:Mapped[DateTime] = mapped_column( DateTime(),default=datetime.utcnow().date())
#     expiry_date:Mapped[DateTime] = mapped_column(DateTime(),default=datetime.utcnow().date() +timedelta(days=60))
    
#     # testing librarian --- other working fine 
#     # librarian_id:Mapped[Integer]=mapped_column(ForeignKey('librarians.id'))
    
#     books = relationship('Book',secondary = 'member_book' , back_populates = 'members')
#     magazines = relationship('Magazine',secondary = 'member_magazine',back_populates = 'members')
#     records = relationship('Record',backref='members')
#     # librarian 
    
#     def __init__(self,name,member_type,email,address,contact_no):
#         self.name=name
#         self.member_type=member_type
#         self.email=email
#         self.address=address
#         self.contact_no=contact_no
    
    
    
     
#     def get_member_by_id(id):
#         member = session.query(Member).filter_by(id=id).first()
#         return member 
     
     
        
    
#     @staticmethod
#     def get_member(email):
#         return session.query(Member).filter_by(email=email).first()
        
    
#     def get_all_members(self):
#         return session.query(Member).all()
        
#     @staticmethod
#     def add_member(name,member_type,email,address,contact_no):
#         member=Member(name,member_type,email,address,contact_no)
#         session.add(member)
#         session.commit()
#         print("Member added Successfully !")
        
        
#     def delete_member(self):
#         member=session.query(Member).filter_by(email=self.email).delete()
#         session.commit()
        
#     def update_member(self,name=None,member_type=None,email=None,address=None,contact_no=None):
#         member=session.query(Member).filter_by(email=self.email).first()
        
#         if member:
#             if name:
#                 member.name=name
                
#             if member_type:
#                 member.member_type=member_type
            
#             if email:
#                 member.email=email
                
#             if address:
#                 member.address=address
                
#             if contact_no:
#                 member.contact_no=contact_no
            
#             session.commit()
            
#         else:
#             print("Member not found !")
            
        
            
    
 
# class Book(Base):
#     __tablename__ = 'books'
    
#     id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
#     isbn:Mapped[int] = mapped_column(nullable=False,unique=True)
#     title:Mapped[str] = mapped_column(nullable=False)
#     author:Mapped[str] = mapped_column(nullable=False)
#     price:Mapped[int] = mapped_column(nullable=False)
#     # is_available:Mapped[bool]=mapped_column(nullable=False)
    
#     members = relationship('Member',secondary = 'member_book',back_populates = 'books')
#     publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
#     publishers = relationship('Publisher',back_populates = 'books')
#     category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
#     categories = relationship('Category',back_populates = 'books')
#     # testing librarians
#     # librarian_id:Mapped[Integer]=mapped_column(ForeignKey('librarians.id'))
#     records = relationship('Record',backref='books')
    
#     def __init__(self,isbn,title,author,price,publisher_id=None,category_id=None ):
#         self.isbn=isbn
#         self.title=title
#         self.author=author
#         self.price=price
#         self.publisher_id=publisher_id
#         self.category_id=category_id
      
    
    
#     @classmethod
#     def get_book(cls,isbn):
#         book=session.query(Book).filter_by(isbn=isbn).first()
#         return cls(book.isbn,book.title,book.author,book.price)
    
#     @staticmethod
#     def get_all_book():
#         return session.query(Book).all()
    
#     @classmethod
#     def add_book(cls,isbn,title,author,price,publisher_id=None,category_id=None):
#         book=cls(isbn=isbn,title=title,author=author,price=price,publisher_id=publisher_id,category_id=category_id)
#         session.add(book)
#         session.commit()
#         print("Book added SucessFull !")
    
    
#     def delete_book(self):
#         book=session.query(Book).filter_by(isbn=self.isbn).delete()
#         session.commit()
        
#     def update_book(self,isbn=None,title=None,author=None,price=None):
#         book=session.query(Book).filter_by(isbn=self.isbn).first()
#         if book:
#             if isbn:
#                 book.isbn=isbn
#             if title:
#                 book.title=title
#             if author:
#                 book.author=author
#             if price:
#                 book.price=price
#             session.commit()
        
#         else:
#             print("Book not Found !!")\
                
#      # borrow_book   
#     def borrow_book(self,member_id,book_id):
#         try:
            
#             book=session.query(Book).filter_by(id=book_id).first()
#             member=session.query(Member).filter_by(id=member_id).first()
            
#             if book is None and member is None:
#                 raise NoResultFound("Both member and book not found  !")
            
#             # check if the member has already borrowed a book with the same ISBN number
#             existing_record=session.query(Record).\
#                 filter(Record.member_id==member_id,Record.returned==False) .\
#                 join(Book,Record.book_id==Book.id) .\
#                 filter(Book.isbn==book.isbn).first()  
                
                
#             if existing_record:
#                 raise Exception (f"{member.name} has already borrowed a copy of {book.title} with the same ISBN number  ")
            
#             book.members.append(member)
#             session.commit()
#             print(f"{member.name} has borrowed {book.title}")
#             # create a record for borrow book 
#             record=Record(member_id=member_id,book_id=book_id,returned=False)
#             session.add(record)
#             session.commit()
#             print("Record add sucessfully !")
            
#         except NoResultFound as e:
#             print(e)
            
#         except Exception as e:
#             print(f"An Error occured :{e}")
            
            
#     def return_book(self,member_id,book_id):
#         try:
#             book=session.query(Book).filter_by(id=book_id).first()
#             member=session.query(Member).filter_by(id=member_id).first()
            
#             if book is None and member is None:
#                 raise NoResultFound("provide both book and magazine")
#             book.members.remove(member)
#             session.commit()
#             print(f"{member.name} has return  {book.title}")
            
#             record=session.query(Record).filter_by(member_id=member_id,book_id=book_id,returned=False).first()
#             if record:
#                 record.returned=True
#                 record.return_date=datetime.utcnow().date()
#                 session.commit()
#                 print("Update returned book sucessfully !")
            
#         except NoResultFound as e:
#             print(e)
        
#         except Exception as e:
#             print("Book and Member not found !")
            
            
   
            
        
# class Magazine(Base):
#     __tablename__ = 'magazines'
    
#     id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
#     issn:Mapped[int] = mapped_column(nullable=False,unique=True)
#     title:Mapped[str] = mapped_column(nullable=False)
#     price:Mapped[int] = mapped_column(nullable=False)
#     editor:Mapped[str] = mapped_column(nullable=False)
#     # is_available:Mapped[bool]=mapped_column(nullable=False)
#     members=relationship('Member',secondary = 'member_magazine',back_populates = 'magazines')    
#     publisher_id:Mapped[int] = mapped_column(ForeignKey('publishers.id'))
#     publishers = relationship('Publisher',back_populates = 'magazines')
#     category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
#     categories = relationship('Category',back_populates = 'magazines')
#     # testing the phase
#     # librarian_id:Mapped[Integer]=mapped_column(ForeignKey('librarians.id'))
    
#     records = relationship('Record',backref='magazines')
    
    
#     def __init__(self,issn,title,price,editor,publisher_id=None,category_id=None):
#         self.issn=issn
#         self.title=title
#         self.price=price
#         self.editor=editor
#         self.publisher_id=publisher_id
#         self.category_id=category_id
        
    
#     @classmethod
#     def get_magazine(cls,issn):
#         magazine=session.query(Magazine).filter_by(issn=issn).first()
#         return cls(magazine.issn,magazine.title,magazine.price,magazine.editor)
       
    
#     @classmethod
#     def add_magazine(cls,issn,title,price,editor,publisher_id=None,category_id=None):
#         magazine=cls(issn=issn,title=title,price=price,editor=editor,publisher_id=publisher_id,category_id=category_id)
#         session.add(magazine)
#         session.commit()
#         print("Magazine added SucessFully !")
        
    
    
#     def show_all_magazine():
#         return session.query(Magazine).all()
    
#     def delete_magazine(self):
#         magazine=session.query(Magazine).filter_by(issn=self.issn).delete()
#         session.commit()
        
#     def update_magazine(self,issn=None,title=None,price=None,editor=None):
#         magazine=session.query(Magazine).filter_by(issn=self.issn).first()
#         if magazine:
#             if issn:
#                 magazine.issn=issn
                
#             if title:
#                 magazine.title=title
                
#             if price:
#                 magazine.price=price
                
#             if editor:
#                 magazine.editor=editor
#             session.commit()
        
#         else:
#             print("Magazine  not Found !!")
            
            
#     def borrow_magazine(self,member_id,magazine_id):
#         try:
#             magazine=session.query(Magazine).filter_by(id=magazine_id).first()
#             member=session.query(Member).filter_by(id=member_id).first()

#             if magazine is None and member is None:
#                 raise NoResultFound("Both member and book not found  !")
                
                
#             existing_record=session.query(Record).\
#                 filter(Record.member_id==member_id,Record.returned==False) .\
#                 join(Magazine, Record.magazine_id==Magazine.id) .\
#                 filter(Magazine.issn==magazine.issn).first()
                
#             if existing_record:
#                     raise Exception (f"{member.name} has already borrowed a copy of {magazine.title} with the same issn number  ")
                
            
#             magazine.members.append(member)
#             session.commit()
#             print(f"{member.name } has borrowed {magazine.title}")
#             # create database for magazine 
#             record=Record(member_id=member_id,magazine_id=magazine_id,returned=False)
#             session.add(record)
#             session.commit()
#             print("Record add Sucessfully ")
            
        
#         except NoResultFound as e:
#             print(e)
            
#         except Exception as e:
#             print(f"No Magazine is found ")
            
#     def return_magazine(self,member_id,magazine_id):
#         try:
#             magazine=session.query(Magazine).filter_by(id=magazine_id).first()
#             member=session.query(Member).filter_by(id=member_id).first()
            
#             if magazine is None and member is None:
#                 raise NoResultFound("Provide both magazine and member ")
#             magazine.members.remove(member)
#             session.commit()
#             print(f"{member.name} has returned {magazine.title}")
#             # find existing magazine here 
#             record=session.query(Record).filter_by(member_id=member_id,magazine_id=magazine_id,returned=False).first()
#             if record: #record bheteu bhane chai tala ko kura change garnu hai ta
#                 record.returned=True
#                 record.return_date=datetime.utcnow().date() #aajha ko date ma book return garyo date change vayo haina ta 
#                 session.commit()
#                 print("updated returned magazine sucessfully ! ")
                    
#         except NoResultFound as e:
#             print(e)       
#         except Exception as e:
#             print("Magazine and Member is not found !")
    
    
            
    
# class Publisher(Base):
#     __tablename__ = 'publishers'
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name:Mapped[str] = mapped_column(unique=True,nullable=False)
#     contact_no:Mapped[str] = mapped_column(String(20),nullable=False)
#     address:Mapped[str] = mapped_column(nullable=False)
#     books = relationship('Book',back_populates = 'publishers')
#     magazines = relationship('Magazine',back_populates = 'publishers')
#     # records = relationship('Records',backref='publishers')
    
#     def __init__(self,name,contact_no,address):
#         self.name=name
#         self.contact_no=contact_no
#         self.address=address
        
    
#     def show_all_publisher():
#         return session.query(Publisher).all()
    
    
#     @classmethod
#     def add_publisher(cls,name,contact_no,address):
#         publisher=cls(name=name,contact_no=contact_no,address=address)
#         session.add(publisher)
#         session.commit()
#         print("Publisher added Sucessfully !")
    
#     @classmethod
#     def get_publisher(cls,name):
#         publisher=session.query(Publisher).filter_by(name=name).first()
#         return cls(publisher.name,publisher.contact_no,publisher.address)
    
#     def delete_publisher(self):
#         publisher=session.query(Publisher).filter_by(name=self.name).delete()
#         session.commit()
        
        
#     def update_publisher(self,name=None,contact_no=None,address=None):
#         publisher=session.query(Publisher).filter_by(name=self.name).first()
#         if publisher:
#             if name:
#                 publisher.name=name
                
#             if contact_no:
#                 publisher.contact_no=contact_no
                
#             if address:
#                 publisher.address=address
                
        
#             session.commit()
        
#         else:
#             print("Publisher  not Found !!")
    


# class Category(Base):
#     __tablename__ = 'category'
    
#     id:Mapped[int] = mapped_column(primary_key=True , autoincrement=True)
#     name:Mapped[str] = mapped_column(unique=True,nullable=False)
#     magazines = relationship('Magazine',back_populates='categories')
#     books = relationship('Book',back_populates='categories')
#     # records = relationship('Records',backref='category')
    
#     def __init__(self,name):
#         self.name=name
    
#     @classmethod
#     def get_category(cls,name):
#         category=session.query(Category).filter_by(name=name).first()
#         return cls(category.name)
    
#     def show_all_category():
#         return session.query(Category).all()
    
#     @classmethod
#     def add_category(cls,name):
#         category=cls(name=name)
#         session.add(category)
#         session.commit()
#         print("Category Added SucessFully !")
        
     
#     def delete_category(self):
#         category=session.query(Category).filter_by(name=self.name).delete()
#         session.commit()
    
#     def update_category(self,name=None):
#         category=session.query(Category).filter_by(name=self.name).first()
#         if category:
#             if name:
#                 category.name=name
                
           
#             session.commit()
        
#         else:
#             print("Category   not Found !!")


    
# class Librarian(Base):
#     __tablename__='librarians'
    
#     id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
#     name:Mapped[str]=mapped_column(nullable=False,unique=True)
#     email:Mapped[str]=mapped_column(nullable=False,unique=True)
#     contact_no:Mapped[int]=mapped_column(nullable=False)
#     # member=relationship('Members',backref='librarian')
#     # book=relationship('Books',backref='librarian')  #librarian =>Librarian (class just a case sensative)
#     # magazine=relationship('Magazine',backref='librarian')
#     # record=relationship('Records',backref='librarian')
    
#     # TODO -manage books -manage magazine - manage records
       
#     def __init__(self,name,contact_no,email):
#         self.name=name
#         self.contact_no=contact_no
#         self.email=email
        
#     @staticmethod
#     def get_email(email):
#         return session.query(Librarian).filter_by(email=email).one_or_none()
        
       
    
# class Record(Base):
#     __tablename__ = 'records'
    
#     id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
#     member_id:Mapped[int] = mapped_column(ForeignKey('members.id'))
#     book_id:Mapped[int] = mapped_column(ForeignKey('books.id'),nullable=True)
#     magazine_id:Mapped[int] = mapped_column(ForeignKey('magazines.id'),nullable=True)
#     returned:Mapped[bool]=mapped_column(nullable=False,default=False)
#     return_date:Mapped[DateTime] = mapped_column(DateTime(),default=datetime.utcnow().date() +timedelta(days=15))
#     borrow_date:Mapped[DateTime] = mapped_column(DateTime(),default = datetime.utcnow().date())
    
#     # testing librarian data 
#     # librarian_id:Mapped[Integer]=mapped_column(ForeignKey('librarians.id'))
    
    
#     def __init__(self,member_id,book_id=None,magazine_id=None,returned=False):
        
#         if not book_id and not magazine_id:
#             raise Exception("No book and Magazine Found  !")
#         self.member_id=member_id
#         self.book_id=book_id
#         self.magazine_id=magazine_id
#         self.returned=returned
        
#     @staticmethod   
#     def show_all_record(member_id):
#         return session.query(Record).filter_by(member_id=member_id).all()
    
#     @staticmethod
#     def show_user_record(member_id):
#         return session.query(Record).filter_by(member_id=member_id,returned=False).all()
    
  
  
  
  
# #   ---------------------Main_File ----------------------------------------------#
# from database import Book,Member,Magazine,MemberBook,MemberMagazine,Record,Librarian,Category,Publisher
# import sys
# import os

# if __name__=='__main__':
    
#     os.system("clear")
#     print("-----Welcome to lms system -----")
#     while True:
#         print('''
#             [1] Register Member
#             [2] Login Member
#             [3] Login  Librarian
#             [4] Exit
        
#             ''')
#         choice=int(input("Enter your choice : "))
        
#         if choice == 1:
#             name=input("Enter your name :")
#             member_type=input("Enter your member type : ")
#             email=input("Enter your email :")
#             address=input("Enter your address :")
#             contact_no=input("Enter your contact_no :")
            
#             new_member=Member.add_member(name,member_type,email,address,contact_no)
#             continue
        
#         elif choice==2:
#             email = input("Enter your email:  ")
#             member = Member.get_member(email)
            
#             while True:
#                 os.system("clear")
#                 print('''
#                     Enter Your Choice :
                    
#                     [1] Show Books
                    
#                     [2] Borrow Book
                    
#                     [3] Return Book
                    
#                     [4] Shows Magazine
                    
#                     [5] Borrow Magazine
                    
#                     [6] Return Magazine
                    
#                     [7] Show my Records
                    
#                     [8] Exit
                    
#                     ''')
                
#                 choice = int(input("Enter your Choice :  "))
#                 if choice == 1:
#                     books = Book.get_all_book()
#                     for book in books:
#                         print(f"{book.title}")
                        
#                 elif choice == 2:
#                     books = Book.get_all_book()
#                     for book in books:
#                         print(f"{book.id} {book.title}")
#                     book_id = int(input('select book with book_id :'))
#                     if member:
#                         book_borrow = Book.borrow_book(Book,member.id,book_id)                  
#                     else:
#                         print("Member not found .Please enter valid email")
                
                        
#                 elif choice == 3:
#                     books = Record.show_user_record(member.id)
#                     for book in books:
#                         if book.book_id:
#                             print(f"{book.book_id}{book.books.title} ")
#                     remove_book_id = int(input("remove book with book_id :"))
#                     if member:
#                         book_return = Book.return_book(Book,member.id,remove_book_id)
                        
            
#                 elif choice==4:
#                     magazines=Magazine.show_all_magazine()
#                     for magazine in magazines:
#                         print(f"{magazine.id} {magazine.title}")
                        
#                 elif choice == 5:
#                     magazines = Magazine.show_all_magazine()
#                     for magazine in magazines:
#                         print(f"{magazine.id} {magazine.title}")   
#                     magazine_id = int(input("select magazine with magazine_id  "))
#                     if member:
#                         magazine_borrow = Magazine.borrow_magazine(Magazine,member.id,magazine_id)
#                     else:
#                         print("Magazine not found !")
                    
                        
#                 elif choice == 6:
#                     magazines = Record.show_user_record(member.id)
#                     for magazine in magazines:
#                         if magazine.magazine_id:
#                             print(f"{magazine.magazine_id} {magazine.magazines.title} ")
#                     remove_magazine_id = int(input("remove magazine with magazine_id :"))
#                     if member:
#                         magazine_return = Magazine.return_magazine(Magazine,member.id,remove_magazine_id)
                                
#                 elif choice == 7:
#                     records=Record.show_all_record(member.id)
#                     for record in records:
#                         print(f"{record.magazine_id} {record.borrow_date} {record.member_id} {record.book_id}")
                        
#                 else:
#                     print("Redirecting back to main menu !")
        
#                     break
                
#         elif choice == 3:
#             email=input("Enter your email ")
            
#             librarian = Librarian.get_email(email)
#             if librarian:
#                 os.system("clear")
#                 print('''
#                     ---Select below Operations---
#                     [1] Add Book
#                     [2] Add Magazine 
#                     [3] Add Member
#                     [4] Add Category
#                     [5] Add Publisher
#                     [6] Exit 
                    
#                     ''')
#                 choice=int(input("Enter your choice : "))
#                 # add book
#                 if choice==1:
#                     isbn=int(input("Enter book isbn number : "))
#                     title=input("Enter book title : ")
#                     author=input("Enter the author : ")
#                     price=int(input("Enter the book price : "))
#                     publisher_id=int(input("Enter publisher_id : "))
#                     category_id=int(input("Enter Category id : "))
                    
#                     new_book=Book.add_book(isbn,title,author,price,publisher_id,category_id)
#                     continue
#                 # add magazine
#                 elif choice==2:
#                     issn=int(input("Enter magazine issn number : "))
#                     title=input("Enter magazine title : ")
#                     price=int(input("Enter the magazine price : "))
#                     editor=input("Enter the magazine editor : ")
#                     publisher_id=int(input("Enter publisher id : "))
#                     category_id=int(input("Enter the category id : "))
                
#                     new_magazine=Magazine.add_magazine(issn,title,price,editor,publisher_id,category_id)
#                     continue              
#                 # add member 
#                 elif choice==3:
#                     name=input("Enter your name : ")
#                     member_type=input("Enter member_type :")
#                     email=input("Enter your email : ") 
#                     address=input("Enter your address : ")
#                     contact_no=input("Enter your contact number :")
                    
#                     new_member=Member.add_member(name,member_type,email,address,contact_no)
#                     continue  
                
#                 #add category
#                 elif choice==4:
#                     name=input("Enter category Name : ")
                    
#                     new_category=Category.add_category(name)
#                     continue
#                 # add publisher 
                
#                 elif choice==5:
#                     name=input("Enter Publisher Name : ")
#                     contact_no=input("Enter Publisher Contact number : ")
#                     address=input("Enter publisher address : ")
                    
#                     new_publisher=Publisher.add_publisher(name,contact_no,address)
#                     continue 
                    
                
                            
                
#         elif choice==4:
            
#             sys.exit("System terminated !")
        
#         else:
#             print("Enter your valid choice !")
#             continue
        
            
    
        
    
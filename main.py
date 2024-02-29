from database import Book,Member,Magazine,MemberBook,MemberMagazine,Record,Librarian,Category,Publisher
import sys
import os
from tabulate import tabulate

if __name__=='__main__':
    
    os.system("clear")
    print("-----Welcome to lms system -----")
    while True:
        print('''
            [1] Register Member
            [2] Login Member
            [3] Login  Librarian
            [4] Exit
        
            ''')
        choice = int(input("Enter your choice : "))
        
        if choice == 1:
            name = input("Enter your name :")
            member_type = input("Enter your member type : ")
            email = input("Enter your email :")
            address = input("Enter your address :")
            contact_no = input("Enter your contact_no :")
            
            new_member = Member.add_member(name,member_type,email,address,contact_no)
            continue
        
        elif choice == 2:
            email = input("Enter your email:  ")
            member = Member.get_member(email)
            
            while True:
                # os.system("clear")
                print('''
                    Enter Your Choice :
                    
                    [1] Show Books
                    [2] Borrow Book
                    [3] Return Book
                    [4] Shows Magazine
                    [5] Borrow Magazine
                    [6] Return Magazine
                    [7] Show my Records
                    [8] Exit
                    
                    ''')
                # show books
                # design added 
                choice = int(input("Enter your Choice :  "))
                if choice == 1:
                    books = Book.get_all_book()
                    final_book=[]
                    for book in books:
                        book_list=[book.isbn,book.title,book.author,book.price]
                        final_book.append(book_list)
                        print("\n")
                    print(tabulate(final_book,headers=['id','isbn','title','author','price']))
                    
                    
                elif choice == 2:
                    books = Book.get_all_book()
                    final_book=[]
                    for book in books:
                        book_list=[book.id,book.title,book.author,book.price]
                        final_book.append(book_list)
                    print(tabulate(final_book,headers=['id','isbn','title','author','price']))
                    print('\n')
                    book_id = int(input('select book with book_id :'))
                    if member:
                        book_borrow = Book.borrow_book(Book,member.id,book_id)                  
                    else:
                        print("Member not found .Please enter valid email")
                
                        #remove book  
                elif choice == 3:
                    books = Record.show_user_record(member.id)
                    final_book=[]
                    for book in books:
                        if book.book_id:
                            book_list=[book.book_id,book.books.title]
                            final_book.append(book_list)
                    print(tabulate(final_book,headers=['book_id','title']))
                    print('\n')
                    remove_book_id = int(input("remove book with book_id :"))
                    if member:
                        book_return = Book.return_book(Book,member.id,remove_book_id)
                        
                                    
                elif choice==4:
                    magazines=Magazine.show_all_magazine()
                    final_magazine=[]                    
                    for magazine in magazines:
                        magazine_list=[magazine.id,magazine.issn,magazine.title,magazine.editor,magazine.price]
                        final_magazine.append(magazine_list)
                    print('\n \n')
                    print(tabulate(final_magazine,headers=['id','issn','title','editor','price']))
                        
                            
                elif choice == 5:
                    magazines = Magazine.show_all_magazine()
                    final_magazine=[]
                    for magazine in magazines:
                        magazine_list=[magazine.id,magazine.issn,magazine.title,magazine.editor,magazine.price]  
                        final_magazine.append(magazine_list)
                    print('\n \n ')
                    print(tabulate(final_magazine,headers=["id",'issn','title','editor','price'])) 
                    
                    print("\n")
                    magazine_id = int(input("select magazine with magazine_id  "))
                    if member:
                        magazine_borrow = Magazine.borrow_magazine(Magazine,member.id,magazine_id)
                    else:
                        print("Magazine not found !")
                    
                        #remove magazine  
                elif choice == 6:
                    magazines = Record.show_user_record(member.id)
                    final_magazine=[]
                    for magazine in magazines:
                        if magazine.magazine_id:
                            magazine_list=[magazine.magazine_id,magazine.magazines.title]
                            magazine_list.append(final_magazine)
                    print(tabulate(final_magazine,headers=['book_id','title']))
                    print('\n')
                    
                    remove_magazine_id = int(input("remove magazine with magazine_id :"))
                    if member:
                        magazine_return = Magazine.return_magazine(Magazine,member.id,remove_magazine_id)
                                
                elif choice == 7:
                    records = Record.show_all_record(member.id)
                    for record in records:
                        print(f"{record.magazine_id} {record.borrow_date} {record.member_id} {record.book_id}")
                        
                else:
                    print("Redirecting back to main menu !")
        
                    break
                
        elif choice == 3:
            email=input("Enter your email ")
            
            librarian = Librarian.get_email(email)
            if librarian:
                os.system("clear")
                print('''
                    ---Select below Operations---
                    [1] Add Book
                    [2] Add Magazine 
                    [3] Add Member
                    [4] Add Category
                    [5] Add Publisher
                    [6] Exit 
                    
                    ''')
                choice=int(input("Enter your choice : "))
                # add book
                if choice == 1:
                    isbn = int(input("Enter book isbn number : "))
                    title = input("Enter book title : ")
                    author = input("Enter the author : ")
                    price = int(input("Enter the book price : "))
                    publisher_id = int(input("Enter publisher_id : "))
                    category_id = int(input("Enter Category id : "))
                    
                    new_book=Book.add_book(isbn,title,author,price,publisher_id,category_id)
                    continue
                # add magazine
                elif choice == 2:
                    issn = int(input("Enter magazine issn number : "))
                    title = input("Enter magazine title : ")
                    price = int(input("Enter the magazine price : "))
                    editor = input("Enter the magazine editor : ")
                    publisher_id = int(input("Enter publisher id : "))
                    category_id = int(input("Enter the category id : "))
                
                    new_magazine = Magazine.add_magazine(issn,title,price,editor,publisher_id,category_id)
                    continue              
                # add member 
                elif choice == 3:
                    name = input("Enter your name : ")
                    member_type = input("Enter member_type :")
                    email = input("Enter your email : ") 
                    address = input("Enter your address : ")
                    contact_no = input("Enter your contact number :")
                    
                    new_member = Member.add_member(name,member_type,email,address,contact_no)
                    continue  
                
                #add category
                elif choice == 4:
                    name = input("Enter category Name : ")
                    
                    new_category = Category.add_category(name)
                    continue
                # add publisher 
                
                elif choice == 5:
                    name = input("Enter Publisher Name : ")
                    contact_no = input("Enter Publisher Contact number : ")
                    address = input("Enter publisher address : ")
                    
                    new_publisher = Publisher.add_publisher(name,contact_no,address)
                    continue 
                    
                
                            
                
        elif choice == 4:
            
            sys.exit("System terminated !")
        
        else:
            print("Enter your valid choice !")
            continue
        
            
    
        
    
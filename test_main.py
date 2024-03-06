from models import Book,Member,Magazine,MemberBook,MemberMagazine,Record,Librarian,Category,Publisher
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
        
        try:
            choice = int(input("Enter your choice : "))

        except ValueError:
            print("Invalid input . Please enter a number ")
            continue

        
        if choice == 1:
            try:
                name = input("Enter your name :")
                member_type = input("Enter your member type : ")
                email = input("Enter your email :")
                address = input("Enter your address :")
                contact_no = input("Enter your contact_no :")
                
                new_member = Member.add_member(name,member_type,email,address,contact_no)


            except Exception as e:
                print(e)
        
        elif choice == 2:
            email = input("Enter your email:  ")
            member = Member.get_member(email)
            if member:
            
                while True:

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
                    try:
                        choice = int(input("Enter your Choice :  "))
                    except ValueError:
                        print("Invalid Input . Please enter a valid number .")
                        continue


                    if choice == 1:
                        os.system("clear")
                        books = Book.get_all_books()
                        final_book=[]
                        for book in books:
                            book_list=[book.isbn,book.title,book.author,book.price]
                            final_book.append(book_list)
                            print("\n")
                        print(tabulate(final_book,headers=['id','isbn','title','author','price']))
                        
                        
                    elif choice == 2:
                        os.system("clear")
                        books = Book.get_all_books()
                        final_book=[]
                        for book in books:
                            book_list=[book.id,book.title,book.author,book.price]
                            final_book.append(book_list)
                        print(tabulate(final_book,headers=['id','isbn','title','author','price']))
                        print('\n')
                        book_id = int(input('select book with book_id :'))
                        book = next((x for x in books if x.id == book_id),None)
                        if member:
                            book_borrow = book.borrow_book(member.id)                  
                        else:
                            print("Member not found .Please enter valid email")
                    


                    elif choice == 3:
                        os.system("clear")
                        books = Record.show_user_record(member.id)
                        final_book=[]
                        for book in books:
                            if book.book_id:
                                book_list=[book.book_id,book.books.title]
                                final_book.append(book_list)
                        print(tabulate(final_book,headers=['book_id','title']))
                        print('\n')

                        remove_book_id = int(input("remove book with book_id :"))

                        book=next((x for x in books if x.book_id ==remove_book_id),None)

                        if book:
                            Book.return_book(book.books,member.id)
                        
                        else:
                            print("Book not found in the record list !")

                            
                    elif choice==4:
                        os.system("clear")
                        magazines=Magazine.show_all_magazines()
                        final_magazine=[]                    
                        for magazine in magazines:
                            magazine_list=[magazine.id,magazine.issn,magazine.title,magazine.editor,magazine.price]
                            final_magazine.append(magazine_list)
                        print('\n \n')
                        print(tabulate(final_magazine,headers=['id','issn','title','editor','price']))
                            

                    elif choice == 5:
                        os.system("clear")
                        magazines = Magazine.show_all_magazines()
                        final_magazine=[]
                        for magazine in magazines:
                            magazine_list=[magazine.id,magazine.issn,magazine.title,magazine.editor,magazine.price]  
                            final_magazine.append(magazine_list)
                        print('\n \n ')
                        print(tabulate(final_magazine,headers=["id",'issn','title','editor','price'])) 
                        
                        print("\n")
                        magazine_id = int(input("select magazine with magazine_id  "))

                        if member:
                            magazine = next((x for x in magazines if x.id==magazine_id),None)
                            magazine_borrow = magazine.borrow_magazine(member.id)
                        else:
                            print("Magazine not found !")
                        
              

                    elif choice == 6:
                        magazines = Record.show_user_record(member.id)
                        final_magazine=[]
                        for magazine in magazines:
                            if magazine.magazine_id:
                                magazine_list=[magazine.magazine_id,magazine.magazines.title]
                                final_magazine.append(magazine_list)
                        print(tabulate(final_magazine,headers=['book_id','title']))
                        print('\n')
                        
                        remove_magazine_id = int(input("remove magazine with magazine_id :"))

                        magazine=next((x for x in magazines if x.magazine_id==remove_magazine_id),None)

                        if magazine:
                           
                            Magazine.return_magazine(magazine.magazines,member.id)
                        else:
                            print("Magazine  record not found ! ")
                

                    elif choice == 7:
                        os.system("clear")
                        records = Record.show_all_records(member.id)
                        final_record=[]
                        for record in records:
                            record_list=[record.member_id,record.borrow_date,record.magazine_id,record.book_id]
                            final_record.append(record_list)
                        print(tabulate(final_record,headers=['member_id','borrow_date','magazine_id','book_id']))
                        print('\n')
                            
                    else:
                        print("Redirecting back to main menu !")
            
                        break
            else:
                print("Please enter valid email !")   


        elif choice == 3:
            email=input("Enter your email ")
            
            librarian = Librarian.get_librarian_by_email(email)
            if librarian:
                while True:
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
                    #  [6] Exit 
                    try:
                        choice=int(input("Enter your choice : "))
                    except ValueError:
                        print("Invalid input . please enter a number !")
                        continue
                    
                    if choice == 1:
                        os.system("clear")
                        try:
                            isbn = int(input("Enter book isbn number : "))
                            title = input("Enter book title : ")
                            author = input("Enter the author : ")
                            price = int(input("Enter the book price : "))
                            publisher_id = int(input("Enter publisher_id : "))
                            category_id = int(input("Enter Category id : "))
                            
                            new_book=Book.add_book(isbn,title,author,price,publisher_id,category_id)


                        except  ValueError as e:
                            print("please check all the information ")


                    elif choice == 2:
                        os.system("clear")
                        try:
                            issn = int(input("Enter magazine issn number : "))
                            title = input("Enter magazine title : ")
                            price = int(input("Enter the magazine price : "))
                            editor = input("Enter the magazine editor : ")
                            publisher_id = int(input("Enter publisher id : "))
                            category_id = int(input("Enter the category id : "))
                        
                            new_magazine = Magazine.add_magazine(issn,title,price,editor,publisher_id,category_id)
                        except ValueError as err:
                            print("Please provide all the information  !")           
                    

                    elif choice == 3:
                        os.system("clear")
                        try:
                            name = input("Enter your name : ")
                            member_type = input("Enter member_type :")
                            email = input("Enter your email : ") 
                            address = input("Enter your address : ")
                            contact_no = input("Enter your contact number :")
                            
                            new_member = Member.add_member(name,member_type,email,address,contact_no)
                        except Exception as err:
                            print(e)
                        

                    elif choice == 4:
                        os.system("clear")
                        try:
                            name = input("Enter category Name : ")
                            new_category = Category.add_category(name)
                        except Exception as e :
                            price(e)
                    

                    elif choice == 5:
                        os.system("clear")
                        try:
                            name = input("Enter Publisher Name : ")
                            contact_no = input("Enter Publisher Contact number : ")
                            address = input("Enter publisher address : ")
                            
                            new_publisher = Publisher.add_publisher(name,contact_no,address)
                        except Exception as err:
                            print(e)

                    elif choice==6:
                        print("Redirecting to main Menu ")
                        break


            else:
                print("Provide a Valid librarian email ")       
                
                                
                
        elif choice == 4:
            
            sys.exit("System terminated !")
        
        else:
            print("Enter your valid choice !")
        
            
    
        
    
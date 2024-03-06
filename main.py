from fastapi import FastAPI,status
from pydantic import BaseModel
from models import Member,Book,Magazine,Publisher,Category,Session,session

app=FastAPI()

# schemas
class MemberModel(BaseModel):
    name:str
    member_type:str
    email:str
    address:str
    contact_no:int
    
class BookModel(BaseModel):
    isbn:int
    title:str
    author:str
    price:int
    publisher_id:int
    category_id:int

class MagazineModel(BaseModel):
    issn:int
    title:str
    editor:str
    price:int
    publisher_id:int
    category_id:int  
    
class PublisherModel(BaseModel):
    name:str
    contact_no:str
    address:str
    
class CategoryModel(BaseModel):
    name:str
    
@app.get('/',tags=['Home'])
async def home():
    return{
        "Members":"/members",
        "Books":"/books",
        "Publisher":"/publisher",
        "Category":"/category",
        
        
    }  
#   for member
  
@app.get("/members/{email}",tags=['Member'])
async def get_member(email):
    return Member.get_member(email=email)


@app.get("/members/",tags=['Member'])
async def show_all_members():
    return Member.get_all_members()


@app.post("/member/",tags=['Member'])
async def add_members(item:MemberModel):
    return{
        "result":Member.add_member(item.name,item.member_type,item.email,item.address,item.contact_no),
    }

# for book
@app.get("/books/{isbn}",tags=['Book'])
async def get_book(isbn):
    return Book.get_book(isbn=isbn)


@app.get("/books/",tags=["Book"])
async def show_all_books():
    return Book.get_all_books()


@app.post('/books/',tags=['Book'])
async def add_book(book:BookModel):
    return{
        "result":Book.add_book(book.isbn,book.title,book.author,book.price,book.publisher_id,book.category_id)
        
    }
    
# for magazine
@app.get('/magazines/{issn}',tags=['Magazine'])
async def get_magazine(issn):
    return Magazine.get_magazine(issn=issn)


@app.get('/magazines/',tags=['Magazine'])
async def show_all_magazines():
    return Magazine.show_all_magazines()
    
@app.post('/magazine',tags=['Magazine'])
async def add_magazine(magazine:MagazineModel):
    return {
        "result":Magazine.add_magazine(magazine.issn,magazine.title,magazine.price,magazine.editor,magazine.publisher_id,magazine.category_id)
    }
    
    
# for publisher 

@app.get("/publishers/{name}",tags=['Publisher'])
async def get_publisher(name):
    return Publisher.get_publisher(name=name)

@app.get("/publishers",tags=['Publisher'])
async def show_all_publisher():
    return Publisher.show_all_publishers()


@app.post("/publisher",tags=['Publisher'])

async def add_publisher(publisher_item:PublisherModel):
    return{
        "result":Publisher.add_publisher(publisher_item.name,publisher_item.contact_no,publisher_item.address)
    }

# for category
@app.get('/category/{name}',tags=['Category'])
async def get_category(name):
    return Category.get_category(name=name)


@app.get('/categories',tags=['Category'])
async def show_category():
    return{
        'result':Category.show_all_categories()
    }
    
@app.post('/categories/',tags=['Category'])
async def add_category(category:CategoryModel):
    return{
        'result':Category.add_category(category.name)
    }
    
    

from typing import Optional
from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field

#Body is used to take input in Query parameters
#path is used to validate path parameters
#Query is used to validate Query parameters
#HTTP Exception returns the status code to the user

app = FastAPI()

# --------------------------------------------------------------

class Book:
    id:str
    title:str
    author:str
    description:str
    rating:int
    publish_date:int

    def __init__(self,id,title,author,description,rating,publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


# --------------------------------------------------------------


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Id is not needed on create",default=None)
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=-1,lt=6)  #(greater than , less than)
    publish_date: int= Field(gt=1499,lt=2027)

    model_config={
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "codingwithruby",
                "description": "A new description of a book",
                "rating": 5,
                "publish_date":2000
            }
        }
    }


# --------------------------------------------------------------



BOOKS = [
    Book(1, 'I Computer Science Pro', 'codingwithroby', 'A very nice book!!', 5,2019),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5,2045),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!!', 5,2017),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2,1823),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3,1997),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1,1674)
]

# --------------------------------------------------------------


@app.get("/books")
async def read_all_books():
    return BOOKS

#FastAPI checks routes in declaration order. 
# Put specific routes such as /books/filterbydate before general dynamic routes such as /books/{book_id}
@app.get("/books/filterbydate")
async def filter_by_publishdate(date:int = Query(gt = 0 , lt = 2500)):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == date:
            books_to_return.append(book)
    return books_to_return



#Use a path parameter when you want to access a specific resource.
@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


#Use a query parameter when you want to filter, sort, search, or customize a request.
@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return



# -----------------------------------------------------


#First we have to validate our data before posting, so the pipeline:
# validate through class BookRequest -> 
# convert it into dict -> get its values -> 
# Convert into Book through Class Book->append it to BOOKS
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))



def find_book_id(book: Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book



#--------------------------------------------------------

@app.put("/books/update_book")
async def update_book(book : BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i]=book



#--------------------------------------------------------

@app.delete("/books/{book_id}")
async def delete_book(book_id:int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            print("Book Deleted")
            break



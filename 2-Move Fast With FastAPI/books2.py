from typing import Optional
from fastapi import FastAPI,Body
from pydantic import BaseModel,Field

app = FastAPI()

# --------------------------------------------------------------

class Book:
    id:str
    title:str
    author:str
    description:str
    rating:int

    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


# --------------------------------------------------------------


class BookRequest(BaseModel):
    id: Optional[str] = None
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=-1,lt=6)  #(greater than , less than)



# --------------------------------------------------------------



BOOKS = [
    Book(1, 'I Computer Science Pro', 'codingwithroby', 'A very nice book!!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]

# --------------------------------------------------------------


@app.get("/books")
async def read_all_books():
    return BOOKS

# --------------------------------------------------------------



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







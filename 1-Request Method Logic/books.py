from fastapi import Body,FastAPI

# CRUD          HTTP Request Method

# Create              POST
# Read                GET
# Update              PUT
# Delete              DELETE



BOOKS = {
    1: {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    2: {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    3: {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    4: {'title': 'Title Four', 'author': 'Author Two', 'category': 'math'},
    5: {'title': 'Title Five', 'author': 'Author One', 'category': 'math'}
}


# To run the code: uvicorn books:app --reload
#uvicorn is the webserver that come with the installation of fast api
app = FastAPI()

@app.get("/books")
async def read_all_books():
    return BOOKS


# Path Parameters-------------------------------------------------

#FastAPI runs from Top to Bottom

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if BOOKS[book].get("title").casefold() == book_title.casefold():
            return BOOKS[book]


# Query Parameters ----------------------------------------------

@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if BOOKS[book].get('category').casefold() == category.casefold():
            books_to_return.append(BOOKS[book])
    return books_to_return



# Both path and Query parameter ----------------------------------
@app.get("/books/{book_author}/")
async def read_author_by_query(book_author:str,category:str):
    books_to_return = []
    for book in BOOKS:
        if BOOKS[book].get('author').casefold() == book_author.casefold() and \
            BOOKS[book].get('category').casefold() == category.casefold():
            books_to_return.append(BOOKS[book])

    return books_to_return


## Post Method ------------------------------------------------

# To post, we use a variable called body and we have to import it
# Get method can not use body
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    new_id = max(BOOKS.keys(), default=0) + 1
    BOOKS[new_id] = new_book
    return {"message": "Book created successfully"}


## Put Method ------------------------------------------------

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(1, len(BOOKS)+1):
        for i in BOOKS:
            if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
                BOOKS[i] = updated_book
                return {"message": "Book updated successfully"}










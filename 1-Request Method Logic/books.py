from fastapi import FastAPI

# CRUD          HTTP Request Method

# Create              POST
# Read                GET
# Update              PUT
# Delete              DELETE



BOOKS = {
    1: {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    2: {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    3: {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    4: {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    5: {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'}
}


# To run the code: uvicorn books:app --reload
#uvicorn is the webserver that come with the installation of fast api
app = FastAPI()

@app.get("/books")
async def read_all_books():
    return BOOKS

#FastAPI runs from Top to Bottom

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if BOOKS[book].get("title").casefold() == book_title.casefold():
            return BOOKS[book]






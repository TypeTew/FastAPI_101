
from fastapi import FastAPI
from pydantic import BaseModel
from routers import book, user, file
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(book.router)
app.include_router(user.router)
app.include_router(file.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def hello():
    return {"message": "Hello World !!!"}

    #python -m pip install virtualenv 
    #virtualenv -p python3 env
    #./env/bin/activate
    
#python3 -m venv env
#pip install fastapi
# uvicorn main:app --reload

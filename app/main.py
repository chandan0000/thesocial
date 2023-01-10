import time
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .databses import engine,get_db 

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating: Optional[int] = None


while True:
    try:

        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="12345",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break

    except Exception as error:
        print("Error while connecting to database")
        print(error)
        time.sleep(2)

my_posts = [
    {
        "title": "My first post",
        "content": "This is my first post",
        "id": 1,
    },
    {
        "title": "favorite foods",
        "content": "I like pazza",
        "id": 2,
    },
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        print(f"{i} - {p}")
        if p["id"] == id:
            return i


# request get method url: "/"
@app.get("/")
def root():
    return {"message": "Hello World"}
@app.get("/sqlalchemy")
def testdb(db:Session=Depends(get_db)):
    post=db.query(models.Post).all()
    print(post)
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post,db:Session=Depends(get_db)):
    
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int,db:Session=Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # post = cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post is id: {id} not found",
        )
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:  {id}  was not found",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post,db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()
    if post1 == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:  {id}  was not found",
        )
    post_query.update(
        post.dict(),
        synchronize_session=False,
    )
    db.commit()

    return post_query.first()
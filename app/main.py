import time
from typing import List
from passlib.context import CryptContext
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .databses import engine,get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)



@app.get("/")
def root():
    return {"message": "Hello World"}



@app.get("/posts",response_model=List[schemas.Post1])
def get_posts(db:Session=Depends(get_db)):

    posts = db.query(models.Post).all()

    return  posts


@app.post("/createpost", status_code=status.HTTP_201_CREATED,response_model=schemas.Post1)
def create_posts(post:schemas.PostBase ,db:Session=Depends(get_db)):
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post


@app.get("/posts/{id}",response_model=schemas.Post1)
def get_post(id: int,db:Session=Depends(get_db)):
 
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post is id: {id} not found", 
        )
    return   post


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db)):
 

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:  {id}  was not found",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=schemas.Post1)
def update_post(id: int, post: schemas.PostBase,db:Session=Depends(get_db)):
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

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    # hash the password - User.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

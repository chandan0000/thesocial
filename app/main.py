from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .databses import engine,get_db
from .router import post,user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/",tags=['Root'])
def root():
    return {"message": "Welcome to apna api"}




# @app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
#     # hash the password - User.password
#     hashed_password=utils.hash(user.password)
#     user.password=hashed_password
#     new_user=models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
# def get_user(id:int ,db:Session=Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id {id} was not found",
#         )
#     return user
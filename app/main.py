from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .databses import engine,get_db
from .router import post,user,auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/",tags=['Root'])
def root():
    return {"message": "Welcome to apna api"}





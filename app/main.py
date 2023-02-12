from fastapi import FastAPI
from . import models
from .databses import engine
from .router import post,user,auth
from .config import settings


app = FastAPI()

models.Base.metadata.create_all(bind=engine)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/",tags=['Root'])
def root():
    return {"message": "Welcome to apna api"}





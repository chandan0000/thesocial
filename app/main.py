from fastapi import FastAPI
from . import models
from .databses import engine
from .router import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

models.Base.metadata.create_all(bind=engine)



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/",tags=['Root'])
def root():
    return {"message": "Welcome to apna api "}


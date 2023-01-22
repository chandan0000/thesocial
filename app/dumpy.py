# import time
# from typing import Optional
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# from fastapi import FastAPI, Response, status, HTTPException
# import psycopg2
# from psycopg2.extras import RealDictCursor
# app = FastAPI()


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating: Optional[int] = None


# while True:
#     try:

#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="12345",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break

#     except Exception as error:
#         print("Error while connecting to database")
#         print(error)
#         time.sleep(2)

# my_posts = [
#     {
#         "title": "My first post",
#         "content": "This is my first post",
#         "id": 1,
#     },
#     {
#         "title": "favorite foods",
#         "content": "I like pazza",
#         "id": 2,
#     },
# ]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         print(f"{i} - {p}")
#         if p["id"] == id:
#             return i


# # request get method url: "/"
# @app.get("/")
# def root():
#     return {"message": "Hello World"}


# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data": posts}


# @app.post("/createpost", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cursor.execute(
#         """INSERT INTO posts(title,content,published) VALUES (%s,%s,%s)""",
#         (post.title, post.content, post.published),
#     )
#     new_post = cursor.fetchone()
#     conn.commit()
#     conn.close()

#     return {"data": new_post}
#     # return {"data": "created post"}


# @app.get("/posts/{id}")
# def get_post(id: str):
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
#     post = cursor.fetchone()
#     print(post)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post is id: {id} not found",
#         )
#     return {"post_details": post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (str(id)))
#     delete_post = cursor.fetchone()
#     conn.commit()
#     if delete_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post is id: {id} not found",
#         )
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute(
#         """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s returning *""",
#         (post.title, post.content, post.published, str(id)),
#     )
#     post = cursor.fetchone()
#     conn.commit()
#     if post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post is id: {id} not found",
#         )

#     return {"message": post}



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
from typing import List, Optional
from fastapi import  Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models,utils,schemas
from ..databses import get_db
from ..oauth2 import get_current_user


router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# @router.get("/",response_model=List[schemas.Post] )
# def get_posts(db: Session = Depends(get_db), current_user:int=Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#     # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
#     #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

#     # cursor.execute("""SELECT * FROM posts """)
#     # posts = cursor.fetchall()

#     # posts = db.execute(
#     #     'select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id  group by posts.id')
#     # results = []
#     # for post in posts:
#     #     results.append(dict(post))
#     # print(results)
#     # posts = db.query(models.Post).filter(
#     #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

#     posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
#         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     return posts
@router.get("/",response_model=List[schemas.Post]) 
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(get_current_user), limit:int=10, 
              skip:int=0,search:Optional[str]=''):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    # filter(models.Post.owner_id ==current_user.id).all( )
    return  posts

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostBase ,current_user:int=Depends(get_current_user),db:Session=Depends(get_db)):
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    # print(f"user id: {post.dict(),current_user.id}")
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session=Depends(get_db),current_user:int=Depends(get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post is id: {id} not found", 
        )
    # if post.owner_id != current_user.id:
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform requested action',)
    return   post


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db),current_user:int=Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:  {id}  was not found",
        )
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform requested action',)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase,current_user:int=Depends(get_current_user),db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:  {id}  was not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform requested action',)
    post_query.update(
        post.dict(),
        synchronize_session=False,
    )
    db.commit()

    return post_query.first()

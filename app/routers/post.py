from .. import models, schemas, utils, oauth2
from fastapi import Body, FastAPI, Response , status, HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
limit: int =10, skip: int =0, search: Optional[str] = "" ):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
    isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search), models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
    print(posts)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED , response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id = current_user.id , **post.dict())  # This is more efficient     # new_post = models.Post(title = post.title, content = post.content, published = post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get("/{id}", response_model= schemas.Post)
@router.get("/{id}", response_model= schemas.PostOut)
def get_one_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(id,))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
    isouter = True).group_by(models.Post.id).filter(models.Post.id == id, models.Post.owner_id == current_user.id)
    post= post_query.first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid id {id}")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesn't exist")
    # print(type(post.owner_id), type(current_user.id))
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {Response(status_code=status.HTTP_204_NO_CONTENT)}


@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title= %s,content=%s, published=%s WHERE id = %s RETURNING *""",( post.title, post.content, post.published, id,))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesn't exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post

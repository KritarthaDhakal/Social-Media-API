from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oath2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Post']
)

# func for reading all posts
@router.get("/", response_model= List[schemas.PostResponse])
def display_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 2, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post, func.count(models.Likes.post_id).label('likes')).join(models.Likes, models.Post.id == models.Likes.post_id, isouter=True).group_by(models.Post.id).all()
    return posts


# func for creating a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(new_post: schemas.CreatePostModel, db: Session = Depends(get_db), current_user: str = Depends(oath2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *""", (new_post.title, new_post.content, new_post.is_published))
    # post = cursor.fetchone()
    # conn.commit()
    post = models.Post(owner_id=current_user.id, **new_post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# func for reading a specific post with id
@router.get("/{id}", response_model=schemas.PostResponse)
def read_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone() 
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Likes.post_id).label('likes')).join(models.Likes, models.Post.id == models.Likes.post_id, isouter=True).group_by(models.Post.id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    return post


# func for updating a post
@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id: int, updated_post: schemas.CreatePostModel, db: Session = Depends(get_db), current_user: str = Depends(oath2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""", (updated_post.title, updated_post.content, updated_post.is_published, id))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post.")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


# func for deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oath2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # post = cursor.fetchone()
    # conn.commit() 
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post.")

    post.delete(synchronize_session=False)
    db.commit()
    return None
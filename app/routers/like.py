from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..oath2 import get_current_user
from ..database import get_db


router = APIRouter(
    prefix="/likes",
    tags=['Like']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(likes: schemas.LikeModel, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    post_exists = db.query(models.Post).filter(models.Post.id == likes.post_id).first()

    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {likes.post_id} does not exist.')
        
    like_query = db.query(models.Likes).filter(models.Likes.post_id == likes.post_id, models.Likes.user_id == current_user.id)
    like_found = like_query.first()

    if likes.like_dir:
        if like_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Post with id {likes.post_id} was already liked by user with id {current_user.id}')
        else: 
            create_like = models.Likes(post_id=likes.post_id, user_id=current_user.id)
            db.add(create_like)
            db.commit()
            return {"message": "Successfully liked post."}
    else:
        if not like_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Like was not found.')
         
        like_query.delete(synchronize_session=False)
        db.commit()
        return {'message': "Successfully deleted post."}

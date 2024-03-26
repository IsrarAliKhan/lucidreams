from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.repo import SessionLocal
from app.database.models import User, Post
from app.models.schemas import PostCreate
from app.auth.auth import get_current_user

router = APIRouter()

@router.post("/addPost/")
def add_post(post: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(SessionLocal)):
    new_post = Post(text=post.text, user_id=current_user.id)
    db.add(new_post)
    db.commit()
    return {"message": "Post added successfully", "post_id": new_post.id}

@router.get("/getPosts/")
def get_posts(current_user: User = Depends(get_current_user), db: Session = Depends(SessionLocal)):
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()
    return posts

@router.delete("/deletePost/{post_id}")
def delete_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(SessionLocal)):
    post_to_delete = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()
    if not post_to_delete:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post_to_delete)
    db.commit()
    return {"message": "Post deleted successfully"}

from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from pydantic import HttpUrl
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import oath2
from .. import models, schemas, oath2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# Get ALL posts from database
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
                 current_user: int = Depends(oath2.get_current_user),
                 limit:int=10, skip:int=0, search:Optional[str] = ""):
    # # This is SQL!
    
    # # Select all posts from database(named posts)
    # cursor.execute(""" SELECT * FROM posts """)
    
    # # Save all posts to variable
    # posts = cursor.fetchall()
    
    # ------------------------------------
       
    # This is ORM!
    
    ## Select all posts from model Post(database named posts)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    ## Authorized users can see only they posts
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # ------------------------------------
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                        models.Post.id==models.Vote.post_id,
    isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # Return posts to user
    return posts


# Create new post and save to database.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oath2.get_current_user)):
    
    # # This is SQL!
    
    # # Insert new post to database
    # cursor.execute(
    #                 """ INSERT INTO posts (title, content, published)
    #                 VALUES (%s, %s, %s) RETURNING * """,
    #                 (post.title, post.content, post.published)
    #                 )
    
    # # new_post is a variable, that fetch created post
    # new_post = cursor.fetchone()
    
    # # Commit our new post to database
    # conn.commit()
    
    # ------------------------------------
    
    # This is ORM!
    
    # Create new post with all columns(unpacked post dictionary **post.dict())
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # Add new post to database
    db.add(new_post)
    # Commit new post
    db.commit()
    # Retrieve to variable new post, that was created and saved to database 
    db.refresh(new_post)
    
    # ------------------------------------
    
    
    # Return new post to user
    return new_post


# Get one post by id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db),
                 current_user: int = Depends(oath2.get_current_user)):
    
    # # This is SQL!
    
    # # Select post by id from our database
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    
    # # Save this post to variable
    # post = cursor.fetchone()
    
    # ------------------------------------
    
    
    # This is ORM!
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                        models.Post.id==models.Vote.post_id,
    isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    # ------------------------------------
    
    
    # Raise an error when post was not found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
        
    # Return post by id to user 
    return post


# Delete post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),
                 current_user: int = Depends(oath2.get_current_user)):
    
    # # This is SQL!    
    
    # # Delete post by id from database
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    
    # # Fetch deleted post
    # deleted_post = cursor.fetchone()
    
    # # Commit deleting
    # conn.commit()
    
    # ------------------------------------
    
    
    # This is ORM!
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    post = post_query.first()
    # Raise an error if post was not exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    # ------------------------------------
    
    # # Raise an error if post was not exist
    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} was not exist")
    
    # Return response to user with 204 status code
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post by id
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oath2.get_current_user)):
    
    # # This is SQL!  
    
    # # Update post by id 
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s 
    #                WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    
    # # Save updated post to variable
    # updated_post = cursor.fetchone()
    
    # # Commit updated post
    # conn.commit()
    
    # ------------------------------------
    
    # This is ORM!
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    updated_post = post_query.first()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to perform requested action")
        
    post_query.update(post.dict(), synchronize_session=False)
    
    db.commit()
    
    # ------------------------------------
    
    
    # # Raise an error if post by id was not exist
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} was not exist")
    
    # Return updated post to user
    return post_query.first()
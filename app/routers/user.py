from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Create user   
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Hash the password = user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    # Create new user with all columns(unpacked user dictionary (pydantic model) => **user.dict())
    new_user = models.User(**user.dict())
    # Add new user to database
    db.add(new_user)
    # Commit new user
    db.commit()
    # Retrieve to variable new user, that was created and saved to database 
    db.refresh(new_user)
    
    return new_user
    

# Get User
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    
    return user
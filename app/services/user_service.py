from fastapi import HTTPException, status

from app.repositories.user_repo import user_repository
from app.models import User, UserRole
from app.core.security import get_password_hash, verify_password, create_access_token
from sqlalchemy.orm import Session

class UserService:
    def __init__(self):
        self.user_repo = user_repository

    def register_user(self, db: Session, user_data: User):
        if self.user_repo.exists_by_email(db, user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="email already exists")
        
        password_hash = get_password_hash(user_data.password)
        user= self.user_repo.create_user(
            db=db, 
            email=user_data.email, 
            password_hash=password_hash, 
            role=UserRole.user )
        return user
    
    def authenticate_user(self, db: Session, email: str, password: str):
        user = self.user_repo.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    def create_user_token(self, user: User):
        access_token = create_access_token(data={"sub": user.email})
        return access_token
    
    def get_user_by_id(self, db: Session, user_id: int):
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id:{user_id} not found"
            )
        
        return user

    def get_user_by_email(self, db: Session, email: str):
        user = self.user_repo.get_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with email:{email} not found"
            )
        return user
    
    def update_user_role(self, db: Session, new_role: UserRole, user_id: int):
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        user.role = new_role
        updated_user = self.user_repo.update(db, user)
        return updated_user
    
    def delete_user(self, db: Session, user_id: int):
        if self.user_repo.delete(db, user_id):
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id {user_id} not found"
            )
    
    def change_password(self, db: Session, user: User, old_password: str, new_password: str):
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="incorect old password"
            )
        
        user.password_hash = get_password_hash(new_password)
        upadated_user = self.user_repo.update(db, user)
        return upadated_user

    def get_user_count(self, db: Session):
        return self.user_repo.count(db)
        

user_service = UserService()

        
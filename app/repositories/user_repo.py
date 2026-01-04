from sqlalchemy.orm import Session
from app.models import User, UserRole

class UserRepository:
    def create_user(self, db: Session, email: str, password_hash: str, role: UserRole = UserRole.user):
        user = User(email= email, password_hash= password_hash, role= role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, user_email: str):
        return db.query(User).filter(User.email == user_email).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()
    
    def update(self, db: Session, user: User):
        db.commit()
        db.refresh(user)
    
    def delete(self, db: Session, user_id: int):
        user = self.get_by_id(db, user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        else:
            return False
    
    def exists_by_email(self, db: Session, email: str):
        user = self.get_by_email(db, email)
        if user: return True
        else: return False

    def count(self, db: Session):
        return db.query(User).count()
    
    def get_by_role(self, db: Session, role: UserRole, skip: int = 0, limit: int = 100):
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()


user_repository = UserRepository()
    
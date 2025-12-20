from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .security import decode_access_token
from app.models.database import get_db
from app.models import User, UserRole
from app.schemas import TokenData
from jose import JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_access_token(token)
        if not payload:
            raise credentials_exception
        
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if not user:
        raise credentials_exception
    return user

async def require_admin(current_user: User = Depends(get_current_user)):
    if User.role != UserRole.admin:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Admin Privileges required"
        )
    return current_user
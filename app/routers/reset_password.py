import secrets
import string
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils import send_reset_email
from app.config import redis_client

router = APIRouter()

def generate_reset_token():
    """Generates a secure random token for password reset."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

@router.post("/auth/reset-password")
def request_password_reset(email: str, db: Session = Depends(get_db)):
    """Request a password reset by generating a token and sending an email."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    reset_token = generate_reset_token()
    redis_client.setex(f"reset_token:{reset_token}", 3600, user.email)  # Token expires in 1 hour
    send_reset_email(user.email, reset_token)
    
    return {"message": "Password reset link sent to your email."}

@router.post("/auth/reset-password/confirm")
def confirm_password_reset(token: str, new_password: str, db: Session = Depends(get_db)):
    """Reset the user's password using a valid reset token."""
    email = redis_client.get(f"reset_token:{token}")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.hashed_password = new_password  # Replace with password hashing logic
    db.commit()
    redis_client.delete(f"reset_token:{token}")  # Remove token after use
    
    return {"message": "Password reset successfully."}

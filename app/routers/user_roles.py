from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user

router = APIRouter()

# Define roles
ROLE_USER = "user"
ROLE_ADMIN = "admin"

def check_admin(user: User):
    """Check if the user has admin privileges."""
    if user.role != ROLE_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

@router.get("/admin/protected")
def admin_only_route(current_user: User = Depends(get_current_user)):
    """Example route accessible only by admins."""
    check_admin(current_user)
    return {"message": "Welcome, Admin!"}

@router.put("/users/set-role/{user_id}")
def set_user_role(user_id: int, role: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Allows an admin to set a user's role."""
    check_admin(current_user)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if role not in [ROLE_USER, ROLE_ADMIN]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    
    user.role = role
    db.commit()
    return {"message": f"User {user_id} role updated to {role}"}

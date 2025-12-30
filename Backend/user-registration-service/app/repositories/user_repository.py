from sqlalchemy.orm import Session
from app.models.user_model import User

class UserRepository:

    @staticmethod
    def save(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

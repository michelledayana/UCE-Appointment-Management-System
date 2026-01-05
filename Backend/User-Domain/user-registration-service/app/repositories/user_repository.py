from app.models.user_model import User

class UserRepository:

    @staticmethod
    def get_by_email(db, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def save(db, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)

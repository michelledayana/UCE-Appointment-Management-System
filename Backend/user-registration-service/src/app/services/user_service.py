from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.kafka.producer import publish_user_registered_event

class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def register_user(self, full_name: str, email: str):
        is_student = email.endswith("@uce.edu.ec")

        user = User(
            full_name=full_name,
            email=email,
            is_student=is_student
        )

        saved_user = self.repository.save(user)
        publish_user_registered_event(saved_user)

        return saved_user

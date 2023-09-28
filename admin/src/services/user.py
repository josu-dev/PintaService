from typing import Optional

from src.core.db import db
from src.core.models.user import User
from src.services.base import BaseService


class UserService(BaseService):
    """Create, read, update and delete users."""

    def get_users(self):
        """Get all users from database"""
        pass

    def get_user(self, user_id: int):
        """Get user from database"""
        pass

    def update_user(self, user_id: int):
        """Update user in database"""
        pass

    def delete_user(self, user_id: int):
        """Delete user from database"""
        pass

    @classmethod
    def create_user(
        cls,
        firstname: str,
        lastname: str,
        password: str,
        email: str,
        username: str,
        document_type: str,
        document_number: str,
        gender: str,
        address: str,
        phone: str,
        gender_other: Optional[str] = None,
        is_active: bool = True,
    ):
        """Create user in database"""
        user = User(
            firstname=firstname,
            lastname=lastname,
            password=password,
            email=email,
            username=username,
            document_type=document_type,
            document_number=document_number,
            gender=gender,
            gender_other=gender_other,
            address=address,
            phone=phone,
            institutions=[],
        )
        db.session.add(user)
        db.session.commit()

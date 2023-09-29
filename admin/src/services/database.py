from sqlalchemy import exc, text

from src.core.db import db
from src.services.base import BaseService


class DatabaseService(BaseService):
    @staticmethod
    def ping() -> bool:
        try:
            db.session.execute(text("SELECT 1")).close()
            return True
        except exc.SQLAlchemyError:
            return False

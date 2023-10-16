from typing import List, Optional, TypedDict

from typing_extensions import Unpack

from src.core.db import db
from src.core.models.service import Service
from src.services.base import BaseService


class ServiceConfig(TypedDict):
    name: str
    laboratory: str
    description: str
    keywords: str
    service_type: str


class ServiceService(BaseService):
    """Service for handling services."""

    @classmethod
    def get_services(cls) -> List[Service]:
        """Get all services from the database."""
        return db.session.query(Service).all()

    @classmethod
    def get_service(cls, service_id: int) -> Optional[Service]:
        """Get a service by its ID."""
        return db.session.query(Service).get(service_id)

    @classmethod
    def update_service(cls, service_id: int, **kwargs: Unpack[ServiceConfig]):
        """Update service in the database."""
        service = db.session.query(Service).get(service_id)
        if service:
            for key, value in kwargs.items():
                setattr(service, key, value)
            db.session.commit()
            return service
        return None

    @classmethod
    def delete_service(cls, service_id: int):
        """Delete service from the database."""
        service = db.session.query(Service).get(service_id)
        if service:
            db.session.delete(service)
            db.session.commit()

    @classmethod
    def create_service(cls, **kwargs: Unpack[ServiceConfig]):
        """Create service in the database."""
        service = Service(**kwargs)
        if ServiceService.get_service(service.id):
            raise Exception("Service already exists")
        db.session.add(service)
        db.session.commit()

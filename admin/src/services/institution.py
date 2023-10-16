from typing import List, Optional, TypedDict

from src.core.db import db
from src.core.models.institution import Institution


class PartialInstitutionConfig(TypedDict):
    name: str
    information: str
    address: str
    location: str
    web: str
    keywords: str
    email: str
    days_and_opening_hours: str


class InstitutionService:
    """Service for handling institutions."""

    @classmethod
    def get_institutions(cls) -> List[Institution]:
        """Get all institutions from the database."""
        return db.session.query(Institution).all()

    @classmethod
    def get_institution(cls, institution_id: int) -> Optional[Institution]:
        """Get an institution by its ID."""
        return db.session.query(Institution).get(institution_id)

    @classmethod
    def create_institution(cls, **kwargs: PartialInstitutionConfig):
        """Create a new institution in the database."""
        institution = Institution(**kwargs)
        if InstitutionService.get_institution(institution.id):
            raise Exception("Institution already exists")
        db.session.add(institution)
        db.session.commit()

    @classmethod
    def update_institution(
        cls, institution_id: int, **kwargs: PartialInstitutionConfig
    ):
        """Update an existing institution in the database."""
        institution = db.session.query(Institution).get(institution_id)
        if institution:
            for key, value in kwargs.items():
                setattr(institution, key, value)
            db.session.commit()
            return institution
        return None

    @classmethod
    def delete_institution(cls, institution_id: int):
        """Delete an institution from the database."""
        institution = db.session.query(Institution).get(institution_id)
        if institution:
            db.session.delete(institution)
            db.session.commit()

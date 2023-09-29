from src.core.db import db
from src.core.models import site


def seed_db():
    site.seed_site_config(db)

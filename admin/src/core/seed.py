from src.core.db import db
from src.core.models import site, user


def seed_db():
    site.seed_site_config(db)
    user.seed_site_users(db)

def seed_db() -> None:
    """Loads seed data into the database.

    This function is used to load required data into the database for the
    application to work properly. This function should be called after the
    database has been created or reseted.
    """
    from src.core.db import db
    from src.core.models import auth, site

    site.seed_site_config(db)
    auth.seed_auth(db)

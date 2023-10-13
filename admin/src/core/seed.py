def seed_db():
    from src.core.db import db
    from src.core.models import auth, site

    site.seed_site_config(db)
    auth.seed_auth(db)

from src.core.enums import DocumentTypes, GenderOptions


def load_test_data():
    import sqlalchemy as sa

    from src.core import enums
    from src.core.db import db
    from src.core.models import auth
    from src.services.auth import AuthService
    from src.services.user import UserService

    UserService.create_user(
        firstname="admin",
        lastname="admin",
        password="admin",
        email="admin@test.test",
        username="admin",
        document_type=enums.DocumentTypes.DNI,
        document_number="12345678",
        gender=enums.GenderOptions.NOT_SPECIFIED,
        address="admin",
        phone="12345678",
        gender_other="",
    )
    db.session.execute(sa.insert(auth.SiteAdmin).values(user_id=1, role_id=1))

    UserService.create_user(
        firstname="test1",
        lastname="test1",
        password="test1",
        email="test1@test.test",
        username="test1",
        document_type=enums.DocumentTypes.DNI,
        document_number="12345678",
        gender=enums.GenderOptions.NOT_SPECIFIED,
        address="test1",
        phone="12345678",
        gender_other="",
    )
    UserService.create_user(
        firstname="test2",
        lastname="test2",
        password="test2",
        email="test2@test.test",
        username="test2",
        document_type=enums.DocumentTypes.DNI,
        document_number="12345678",
        gender=enums.GenderOptions.OTHER,
        address="test2",
        phone="12345678",
        gender_other="test2",
    )

    UserService.create_user(
        firstname="noperm",
        lastname="noperm",
        password="noperm",
        email="noperm@test.test",
        username="noperm",
        document_type=enums.DocumentTypes.DNI,
        document_number="12345678",
        gender=enums.GenderOptions.NOT_SPECIFIED,
        address="noperm",
        phone="12345678",
        gender_other="",
    )

    UserService.create_user(
        firstname="Luciano Ariel",
        lastname="Lopez",
        password="1234",
        email="waderlax@hotmail.com",
        username="waderlax",
        document_type=enums.DocumentTypes.DNI,
        document_number="40188236",
        gender=enums.GenderOptions.MALE,
        gender_other="tal vez",
        address="155",
        phone="2213169050",
    )
    UserService.create_user(
        firstname="Luciano",
        lastname="Lopez",
        password="1234",
        email="lucholopezlp@hotmail.com",
        username="lucho",
        document_type=enums.DocumentTypes.DNI,
        document_number="40188236",
        gender=enums.GenderOptions.FEMALE,
        gender_other="",
        address="155",
        phone="2213169050",
    )
    UserService.create_user(
        firstname="Franco",
        lastname="Cirielli",
        password="1234",
        email="franco@hotmail.com",
        username="francry",
        document_type=DocumentTypes.DNI,
        document_number="25683652",
        gender=GenderOptions.FEMALE,
        gender_other="tal vez",
        address="15 y 47",
        phone="2355572726",
    )
    UserService.create_user(
        firstname="Bolivia",
        lastname="Nose",
        password="1234",
        email="inaki@gmail.com",
        username="Vargas",
        document_type=DocumentTypes.DNI,
        document_number="40188236",
        gender=GenderOptions.FEMALE,
        gender_other="",
        address="155",
        phone="2213169050",
    )

    from src.core.models import institution

    ins1 = institution.Institution(
        name="Institución 1",
        address="Calle 1",
        days_and_opening_hours="Lunes a Viernes de 8:00 a 17:00",
        information="Información de la institución 1",
        location="Lugar 1",
        web="https://www.institucion1.com",
        keywords="institucion1, institucion, 1",
        email="ins1@ins1.com",
    )
    ins2 = institution.Institution(
        name="Institución 2",
        address="Calle 2",
        days_and_opening_hours="Lunes a Viernes de 8:00 a 17:00",
        information="Información de la institución 2",
        location="Lugar 2",
        web="https://www.institucion2.com",
        keywords="institucion2, institucion, 2",
        email="ins2@ins2.com",
    )
    db.session.add(ins1)
    db.session.add(ins2)
    db.session.commit()

    AuthService.add_institution_role(
        "OWNER", user_id=2, institution_id=ins1.id
    )
    AuthService.add_institution_role(
        "OWNER", user_id=2, institution_id=ins2.id
    )
    AuthService.add_institution_role(
        "OWNER", user_id=3, institution_id=ins2.id
    )

    # UserService.create_user(
    #     firstname="test",
    #     lastname="test",
    #     password="test",
    #     email="test@test.com",
    #     username="test",
    #     document_type=DocumentTypes.DNI,
    #     document_number="25683652",
    #     gender=GenderOptions.FEMALE,
    #     gender_other="tal vez",
    #     address="15 y 47",
    #     phone="2355572726",
    # )

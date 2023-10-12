from src.core.enums import DocumentTypes, GenderOptions


def load_test_data():
    from src.services.user import UserService

    UserService.create_user(
        firstname="Luciano Ariel",
        lastname="Lopez",
        password="1234",
        email="waderlax@hotmail.com",
        username="waderlax",
        document_type=DocumentTypes.DNI,
        document_number="40188236",
        gender=GenderOptions.MALE,
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
        document_type=DocumentTypes.DNI,
        document_number="40188236",
        gender=GenderOptions.FEMALE,
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

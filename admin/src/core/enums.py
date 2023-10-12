from enum import Enum


class GenderOptions(Enum):
    MALE = "Masculino"
    FEMALE = "Femenino"
    OTHER = "Otros(Por favor especifica)"
    NOT_SPECIFIED = "Prefiero no decir"


class DocumentTypes(Enum):
    DNI = "DNI"
    LC = "Libreta Civica"
    LE = "Libreta de Enrolamiento"


class ServiceType(Enum):
    ANALYSIS = "analisis"
    CONSULTANCY = "consultoria"
    DEVELOPMENT = "desarrollo"

import enum


class RoleEnum(enum.Enum):
    SITE_ADMIN = "SITE_ADMIN"
    OWNER = "INSTITUTION_OWNER"
    MANAGER = "INSTITUTION_MANAGER"
    OPERATOR = "INSTITUTION_OPERATOR"


class ActionEnum(enum.Enum):
    INDEX = "index"
    SHOW = "show"
    CREATE = "create"
    UPDATE = "update"
    DESTROY = "destroy"
    ACTIVATE = "activate"
    DEACTIVATE = "deactivate"


class ModuleEnum(enum.Enum):
    USER = "user"
    INSTITUTION = "institution"
    USER_INSTITUTION = "user_institution"
    SERVICES = "services"
    SERVICE_REQUEST = "service_request"
    SETTING = "setting"


MODULE_ACTIONS = {
    ModuleEnum.USER: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.INSTITUTION: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
        ActionEnum.ACTIVATE,
        ActionEnum.DEACTIVATE,
    ),
    ModuleEnum.USER_INSTITUTION: (
        ActionEnum.INDEX,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.SERVICES: (
        ActionEnum.INDEX,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.SERVICE_REQUEST: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.SETTING: (
        ActionEnum.SHOW,
        ActionEnum.UPDATE,
    ),
}

ROLE_MODULE_PERMISSIONS = {
    RoleEnum.SITE_ADMIN: {
        ModuleEnum.USER: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.INSTITUTION: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
            ActionEnum.ACTIVATE,
            ActionEnum.DEACTIVATE,
        ),
        ModuleEnum.SETTING: (
            ActionEnum.SHOW,
            ActionEnum.UPDATE,
        ),
    },
    RoleEnum.OWNER: {
        ModuleEnum.USER_INSTITUTION: (
            ActionEnum.INDEX,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.SERVICES: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.SERVICE_REQUEST: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
    },
    RoleEnum.MANAGER: {
        ModuleEnum.SERVICES: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.SERVICE_REQUEST: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
    },
    RoleEnum.OPERATOR: {
        ModuleEnum.SERVICES: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
        ),
        ModuleEnum.SERVICE_REQUEST: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.UPDATE,
        ),
    },
}

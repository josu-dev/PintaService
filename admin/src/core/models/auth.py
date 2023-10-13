import flask_sqlalchemy as fsa
import sqlalchemy as sa
import sqlalchemy.orm as sao

from src.core.models import base


class UserInstitutionRole(base.BaseModel):
    __tablename__ = "users_institutions_roles"

    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, init=False)
    user_id: sao.Mapped[int]
    institution_id: sao.Mapped[int]
    role_id: sao.Mapped[int]

    __table_args__ = (sa.UniqueConstraint("user_id", "institution_id"),)


class SiteAdmin(base.BaseModel):
    __tablename__ = "site_admins"

    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, init=False)
    user_id: sao.Mapped[int] = sao.mapped_column(unique=True)
    role_id: sao.Mapped[int]


class RolePermission(base.BaseModel):
    __tablename__ = "roles_permissions"

    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, init=False)
    role_id: sao.Mapped[int]
    permission_id: sao.Mapped[int]


class Role(base.BaseModel):
    __tablename__ = "roles"

    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, init=False)
    name: sao.Mapped[str] = sao.mapped_column(sa.String(64), unique=True)


class Permission(base.BaseModel):
    __tablename__ = "permissions"

    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, init=False)
    name: sao.Mapped[str] = sao.mapped_column(sa.String(64), unique=True)


def seed_auth(db: fsa.SQLAlchemy):
    from src.core.permissions import (
        MODULE_ACTIONS,
        ROLE_MODULE_PERMISSIONS,
        RoleEnum,
    )

    permissions = tuple(
        {"name": f"{module.value}_{action.value}"}
        for module, actions in MODULE_ACTIONS.items()
        for action in actions
    )

    db.session.execute(sa.insert(Permission), permissions)

    roles = tuple({"name": role.value} for role in RoleEnum)

    db.session.execute(sa.insert(Role), roles)

    for role, modules in ROLE_MODULE_PERMISSIONS.items():
        actions = tuple(
            f"{module.value}_{action.value}"
            for module, actions in modules.items()
            for action in actions
        )
        role_permissions = tuple(
            p
            for p in db.session.execute(
                sa.select(Permission.id).where(Permission.name.in_(actions))
            ).scalars()
        )
        role_id = db.session.execute(
            sa.select(Role.id).where(Role.name == role.value)
        ).scalar_one()

        db.session.execute(
            sa.insert(RolePermission),
            tuple(
                {"role_id": role_id, "permission_id": permission_id}
                for permission_id in role_permissions
            ),
        )

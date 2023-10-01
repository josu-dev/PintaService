import typing_extensions as te
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField
from wtforms import validators as v

from src.services.site import PartialSiteConfig


class SiteUpdateForm(FlaskForm):
    page_size = IntegerField(
        "Tamaño de pagina",
        validators=[v.DataRequired(), v.NumberRange(min=1, max=100)],
    )
    contact_info = StringField(
        "Informacion de contacto",
        validators=[v.Length(min=0, max=256)],
    )
    maintenance_active = BooleanField("En mantenimiento")
    maintenance_message = StringField(
        "Mensaje de mantenimiento",
        validators=[v.Length(min=0, max=512)],
    )

    def values(self) -> PartialSiteConfig:
        config = PartialSiteConfig(
            page_size=te.cast(int, self.page_size.data),
            contact_info=te.cast(str, self.contact_info.data),
            maintenance_active=self.maintenance_active.data,
            maintenance_message=te.cast(str, self.maintenance_message.data),
        )

        return config

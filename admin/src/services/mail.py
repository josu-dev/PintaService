import smtplib

import jinja2
from flask import Flask, render_template_string
from flask_mail import Mail, Message

from src.services.base import BaseService, BaseServiceError

EMAIL_RENDERING_ERROR = "El renderizado del template para el body fallo"
EMAIL_SMTP_ERROR = "El envio del mail fallo"


class MailServiceError(BaseServiceError):
    pass


class MailService(BaseService):
    """Service for handling mail sending.

    This service is used for sending emails as the configured sender.
    """

    _mail: Mail
    MailServiceError = MailServiceError

    @classmethod
    def init_app(cls, app: Flask) -> None:
        cls._mail = Mail()
        cls._mail.init_app(app)

    @classmethod
    def send_mail(
        cls,
        subject: str,
        recipients: str,
        body: str,
    ) -> None:
        """Sends an email.

        Args:
            subject: The subject of the email.
            recipients: The recipients of the email.
            body: The body of the email, a jinja2 template string.

        Raises:
            MailServiceError: If the email could not be sent.
        """
        try:
            html = render_template_string(body)
        except jinja2.TemplateError as e:
            raise MailServiceError(e.message or EMAIL_RENDERING_ERROR)
        msg = Message(
            subject=subject,
            recipients=[recipients],
            html=html,
        )
        try:
            cls._mail.send(msg)
        except smtplib.SMTPException as e:
            raise MailServiceError(e.strerror or EMAIL_SMTP_ERROR)

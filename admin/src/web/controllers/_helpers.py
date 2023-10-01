import flask


def flash_info(message: str):
    flask.flash(message, "info")


def flash_success(message: str):
    flask.flash(message, "success")


def flash_warning(message: str):
    flask.flash(message, "warning")


def flash_error(message: str):
    flask.flash(message, "error")

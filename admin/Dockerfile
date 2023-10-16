FROM python:3.8

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
  PYTHONUNBUFFERED=1

ENV FLASK_RUN_PORT=5000

RUN pip install poetry==1.6.1

COPY pyproject.toml poetry.lock ./
COPY static ./static
COPY src ./src
COPY app.py ./app.py
COPY tailwind.config.js ./tailwind.config.js
RUN touch README.md

RUN poetry install

RUN poetry run flask-livetw build

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--debug", "--host=0.0.0.0"]

# ENV LIVETW_DEV=true
#
# EXPOSE 5678
#
# CMD ["poetry", "run", "flask-livetw", "dev", "--flask-host=0.0.0.0"]

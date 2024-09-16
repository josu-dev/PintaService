FROM python:3.12-alpine

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

WORKDIR /app

COPY requirements-dev.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY pyproject.toml .
COPY tailwind.config.js .
COPY static ./static
COPY src ./src

RUN livetw build

EXPOSE $PORT

CMD gunicorn -b :$PORT "src.web:create_app(env='production')"

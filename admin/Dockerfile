FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV PORT=5000

WORKDIR /app

COPY requirements-dev.txt requirements.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY src ./src
COPY static ./static
COPY app.py .
COPY pyproject.toml .
COPY tailwind.config.js .

RUN flask-livetw build

EXPOSE $PORT

CMD gunicorn -b :$PORT 'src.web:create_app(env="production")'

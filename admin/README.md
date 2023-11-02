![Pinta Service Logo](./static/img/logo_256x256.png)

# Admin

The Admin module is the private application for managing the public website for the services of [CIDEPINT](https://cidepint.ing.unlp.edu.ar/).

## Quick Start

1. Install Poetry.
2. Install dependencies: Run `poetry install`.
3. Create a `.env` file from the provided `.env.example`.
4. Run Docker Compose: Use `docker compose up -d` or add a custom database and mail server in the `.env` file.
5. Initialize the database: Run `poetry run flask reset-db` and `poetry run flask seed-db`.
6. Start the application: Use `poetry run flask run` for a production-like environment or `poetry run flask-livetw dev` for a development-like environment.
7. Open the application in your browser at `http://localhost:5000`.

## Detailed Guide

For more information, refer to the detailed guide in the [Backend Documentation](../docs/BACKEND.md).

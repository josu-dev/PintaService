![Pinta Service Logo](./static/img/logo_256x256.png)

# Admin

The admin module is the private application for the administration of the public website for the services of [CIDEPINT](https://cidepint.ing.unlp.edu.ar/).


## Quick start

1. Install poetry
2. Install dependencies: `poetry install`
3. Create a `.env` from `.env.example`
4. Run docker compose: `docker compose up -d` or add a custom db and mail server in `.env`
5. Initialize the database: `poetry run flask reset-db` and `poetry run flask seed-db`
5. Start the application: `poetry run flask run` for a production like enviroment or `poetry run flask-livetw dev` for a development like environment
6. Open the application in your browser at `http://localhost:5000`


## Detailed guide

A detailed guide can be found in the [backend documentation](../docs/BACKEND.md).

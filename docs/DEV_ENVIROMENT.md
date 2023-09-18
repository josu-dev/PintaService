# Developer enviroment

This document describes how to setup the developer enviroment.


<br/>

## Enviroment variables

The following enviroment variables are required:

```ini
# postgres config
DB_HOST=localhost
DB_PORT=5432
DB_USER=dev
DB_PASS=password
DB_NAME=service_search

# pgadmin config
PGADMIN_PORT=5050
PGADMIN_DEFAULT_EMAIL=dev@dev.com
PGADMIN_DEFAULT_PASSWORD=password
```

> **Note 1:** The values above are examples, can be changed to whatever you want.
>
> **Note 2:** If some of the variables related to postgres and pgadmin are missing or empty, the defaults of the docker compose file will be used.


<br/>

## Database

The database is intended to be run using docker.

To install docker, simple go to the [docker website](https://www.docker.com/) and follow the instructions.

> **Note:** If you are using Windows, you will need to install wsl, running `wsl --install`

### Running the database and pgadmin

The database as well as the pgadmin can be run using the docker compose file.

To run the database, run the following command:

```bash
docker-compose up -d
```

> **Note 1:** The database and pgadmin will be configured using the enviroment variables described above.
>
> **Note 2:** The `-d` flag is to detach the process from the terminal, so it can run in the background.

### Using pgadmin

To access the pgadmin, open your browser and go to `http://127.0.0.1:5050`.


<br/>

## Database administration

To administrate the database download [pgAdmin](https://www.pgadmin.org/download/).

To connect to the database, open pgAdmin and click on the "Add New Server" button.

Fill the form with the following information:

Initial panel:
- **Name:** service_search

Connection panel:
- **Host name/address:** postgres
- **Port:** 5432
- **Username:** dev
- **Password:** password

Click on the "Save" button.


<br/>

## Editor setup (VSCode)

### Recommend extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Black formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Better Jinja](https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml)
- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)

### Settings for extensions:

Use local settings to override the default settings.

Local settings files:

- `.vscode/settings.json` (project root settings)
- `admin/.vscode/settings.json` (inside admin folder settings)

Minimal settings:
```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "black-formatter.args": [
    "--line-length=79",
  ],
  "emmet.includeLanguages": {
    "jinja-html": "html"
  },
  "files.associations": {
    "*.j2.html": "jinja-html"
  },
  "isort.args": [
    "--profile",
    "black"
  ]
}
```

Extra settings:

```json
{
  "files.autoSaveDelay": 30000,
  "files.exclude": {
    "**/.pytest_cache": true,
    "**/__pycache__": true
  },
  "python.analysis.typeCheckingMode": "strict",
  "tailwindCSS.includeLanguages": {
    "jinja-html": "html",
    "plaintext": "jinja-html"
  }
}
```

### Set poetry to use local environment

Its recommended to use the local environment inside the project so vscode can easily find the environment.

Open a terminal and run the following command:

```bash
poetry config virtualenvs.in-project true
```

> **Note:** `cwd` must be the root of the project (where the `pyproject.toml` file is located).

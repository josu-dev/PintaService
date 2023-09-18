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


<br/>

## Database

The database is preferably run in a docker container.

To install docker, simple go to the [docker website](https://www.docker.com/) and follow the instructions.

> **Note:** If you are using Windows, you will need to install wsl, running `wsl --install`

### Installing the database

To install the database image, run the following command:

```bash
docker pull postgres
```

> **Note:** If its the first time you are running docker, open the docker desktop app and finish the setup.

### Running the database

Run the following command:

```bash
docker run --name service-search -e POSTGRES_PASSWORD=password -e POSTGRES_DB=service-search -p 5432:5432 -d postgres
```


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

Open a terminal and run the following command:

```bash
poetry config virtualenvs.in-project true
```

> **Note:** `cwd` must be the root of the project (where the `pyproject.toml` file is located).

# Developer enviroment

This document describes the development enviroment and how to setup the tools used in the project.


<br/>

## Backend - _'admin/'_

This section describes how to setup the backend related development enviroment and how to run the related tools.

Some important files/folders:

```text
admin/
├── src/                      # source code
├── static/                   # static files used in the templates
├── .env                      # enviroment variables for configuration
├── .pre-commit-config.yaml   # pre-commit configuration of git hooks
├── compose.yaml              # docker compose for database and pgadmin
├── dev.py                    # dev server script
├── pyproject.toml            # poetry and tools configuration
└── tailwind.config.js        # tailwindcss configuration for the templates
```


<br/>

### Poetry

Poetry is the tool used to manage the python dependencies and virtual enviroments for the project.

To install poetry, follow the official [poetry installation guide](https://python-poetry.org/docs/#installation).

After installing poetry is recommended to run the following command to configure the virtual enviroments to be created inside the project folder:

```bash
poetry config virtualenvs.in-project true
```

> **Note:** `cwd` must be the root of the project (where the `pyproject.toml` file is located).

To install the dependencies, run the following command:

```bash
poetry install
```


<br/>

### Enviroment variables

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

### Database

The database is intended to be run using docker.

To install docker, simple go to the [docker website](https://www.docker.com/) and follow the instructions.

> **Note:** If you are using Windows, you will need to install wsl, running `wsl --install`


#### Running the database and pgadmin

The database as well as the pgadmin can be run using the docker compose file.

To run the database, run the following command:

```bash
docker compose up -d
```

> **Note 1:** The database and pgadmin will be configured using the enviroment variables described above.
>
> **Note 2:** The `-d` flag is to detach the process from the terminal, so it can run in the background.
>
> **Note 3:** The `cwd` must be `<project_root>/admin/` folder (where the `compose.yaml` file is located).


#### Using pgadmin

If you started the database and pgadmin using the docker compose file, you can access the pgadmin using at `http://localhost:5050` (or the port you configured) otherwise you must configure the pgadmin manually.

Once you are in the pgadmin login page, login using the credentials you configured in the enviroment variables.

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

### Editor setup (VSCode)

#### Recommend extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Black formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Better Jinja](https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml)
- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)


#### Settings for extensions:

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
    "--profile=black",
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

> **Note:** The .vscode folder is ignored by git, so you can add your own settings without worrying about commiting them.


<br/>

### pre-commit

The pre-commit is a tool that runs a set of checks before commiting the code ([git hooks](https://git-scm.com/docs/githooks)).

To install the pre-commit, run the following command:

```bash
pre-commit install
```

> **Note 1:** `cwd` must be the root of the project (where the `pre-commit-config.yaml` file is located).
>
> **Note 2:** If fails to run, try starting a poetry shell first (`poetry shell`).
>
> **Note 3:** In order to work properly you must have installed the dev dependencies (`poetry install`).

If you want to run the pre-commit manually, run the following command:

```bash
pre-commit run --all-files
```

If you want to type check the code before pushing you can install the pre-push hook:

```bash
pre-commit install --hook-type pre-push
```

> **Note:** To uninstall the pre-push hook, run `pre-commit uninstall --hook-type pre-push`.


<br/>

### Dev server

The dev server generates the tailwindcss file on template changes and triggers the client (browser page) to reload in order to apply the changes.

To run the backend in Dev mode run:

```bash
python dev.py dev

# or

./dev.py dev
```

> **Note 1:** The `cwd` must be `<project_root>/admin/` folder (where the `dev.py` file is located).
>
> **Note 2:** If fails to run, try starting a poetry shell first (`poetry shell`).


#### Build for production

Building for production in this case means to generate a minimized version of the tailwindcss file.

To build for production run:

```bash
python dev.py build

# or

./dev.py build
```

> **Note:** Same notes as the dev server.


<br/>

## Frontend - _'folder_name/'_

_Will be added at some point..._

# Backend


This document describes the development enviroment, files/folders layout (structure) and tools used in the backend of the project.

The backend is a [Flask](https://flask.palletsprojects.com/en/2.0.x/) application that uses [SQLAlchemy](https://www.sqlalchemy.org/) as the ORM and [Tailwindcss](https://tailwindcss.com/) as the CSS framework.

The python version used in the project is `3.8.10`.

This document assumes that your working directory is the root of the project (where the `admin/` folder is located).

Some of the most important files/folders are:

```text
🌳 admin/
┣ 📁 src/
┣ 📁 static/
┣ 📄 .env
┣ 📄 .pre-commit-config.yaml
┣ 📄 app.py
┣ 📄 compose.yaml
┣ 📄 pyproject.toml
┗ 📄 tailwind.config.js
```

- `admin/`: This folder contains the backend of the project.
  - `src/`: This folder contains the source code of the backend.
  - `static/`: This folder contains the static files for the project.
  - `.env`: This file contains the enviroment variables for the project (sentitive data).
  - `.pre-commit-config.yaml`: This file contains the pre-commit configuration for the project. This configuration is used to run the linters and formatters before commiting the changes to the repository. This configuration is used to enforce the code style and format.
  - `app.py`: This file contains the flask entry point for the project during development, on production this file is replaced for the `create_app` function in the `src/web/__init__.py` file.
  - `compose.yaml`: This file contains the docker compose definition to run the database and pgadmin for development.
  - `pyproject.toml`: This file contains the poetry and tools configuration for the project.
  - `tailwind.config.js`: This file contains the tailwindcss configuration for the project used in the templates.

> **Note:** A more detailed description of the files/folders can be found in the [Project layout](#project-layout) section.


<br />

## Table of contents:

- [Development enviroment](#development-enviroment)
  - [Pyenv](#pyenv)
  - [Poetry](#poetry)
  - [Enviroment variables](#enviroment-variables)
  - [Database](#database)
    - [Running the database and pgadmin](#running-the-database-and-pgadmin)
    - [Using pgadmin](#using-pgadmin)
    - [Resetting the database](#resetting-the-database)
  - [Editor setup (VSCode)](#editor-setup-vscode)
  - [pre-commit](#pre-commit)
  - [Development server](#development-server)
  - [Build for production](#build-for-production)
  - [Development Mail server](#development-mail-server)
- [Project layout](#project-layout)
- [Questions and Answers](#questions-and-answers)


<br/>

## Development enviroment


<br/>

### Pyenv

Pyenv is the tool used to manage the python versions for the project.

To install pyenv, follow the official [pyenv installation guide](https://github.com/pyenv/pyenv#installation).

After installing pyenv is recommended to run the following command to configure the virtual enviroments to be created inside the project folder

```bash
pyenv local 3.8.10
```


<br/>

### Poetry

Poetry is the tool used to manage the python dependencies and virtual enviroments for the project.

To install poetry, follow the official [poetry installation guide](https://python-poetry.org/docs/#installation).

After installing poetry is recommended to run the following command to configure the virtual enviroments to be created inside the project folder:

```bash
poetry config virtualenvs.in-project true
```

To install the dependencies, run the following command:

```bash
poetry install
```


<br/>

### Enviroment variables

Required enviroment variables:

```ini
# Postgres
DB_HOST=localhost
DB_USER=dev
DB_PASS=password
DB_NAME=service_search

# pgAdmin (development only)
PGADMIN_PORT=5050
PGADMIN_DEFAULT_EMAIL=dev@dev.com
PGADMIN_DEFAULT_PASSWORD=password

# Flask
SECRET_KEY='development key'

# WTForms
WTF_CSRF_ENABLED='True'
WTF_CSRF_SECRET_KEY='development key'

# Flask-Mail config
MAIL_SERVER="localhost"
MAIL_PORT=1025
MAIL_USE_SSL=False
MAIL_USE_TLS=False
MAIL_USERNAME="development username"
MAIL_PASSWORD="development password"
MAIL_DEFAULT_SENDER="development@mail.com"
```

Optional enviroment variables:

```ini
# Postgres
DB_PORT=5432

# Flask-Session
SESSION_TYPE=filesystem
```

> **Note 1:** The values above are examples, can be changed to whatever you want.
>
> **Note 2:** If some of the variables related to postgres and pgadmin are missing or empty, the defaults of the docker compose file will be used instead during development.


<br/>

### Database

The database is intended to be run using docker during development.

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

> **Note:** The values above are the defaults, if you changed the values in the enviroment variables, you must use the new values instead.

#### Resetting the database

To reset the database, run the following command:

```bash
flask reset_db
```

To seed the database, run the following command:

```bash
flask seed_db
```

> **Note:** This maybe change in the future.


<br/>

### Editor setup (VSCode)

Recommended extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Black formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Better Jinja](https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml)
- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)


Its recommended to create a local settings file for the project at `.vscode/settings.json` or in `admin/.vscode/settings.json` if you want to open the project from the admin folder. Creating a local settings file allows you to customize the settings without affecting the global settings.

The settings are for the editor itself and the extensions.

Required settings:

```json
{
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": "always"
    },
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "black-formatter.args": [
    "--line-length=79",
  ],
  "editor.formatOnSave": true,
  "emmet.includeLanguages": {
    "jinja-html": "html"
  },
  "files.associations": {
    "*.j2.html": "jinja-html"
  },
  "flake8.args": [
    "--ignore=W503"
  ],
  "isort.args": [
    "--profile=black",
    "--line-length=79",
    "--src-path=./admin/"
  ],
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingTypeStubs": "information",
    "reportUnknownMemberType": "none",
    "reportUnusedFunction": "none"
  },
  "python.analysis.extraPaths": [
    "./admin/"
  ],
  "tailwindCSS.includeLanguages": {
    "jinja-html": "html",
    "plaintext": "jinja-html"
  }
}
```

Optional settings:

```json
{
  "files.autoSaveDelay": 30000,
  "files.exclude": {
    "**/.pytest_cache": true,
    "**/__pycache__": true
  },
  "python.analysis.typeCheckingMode": "strict"
}
```

The .vscode folder is ignored by git, so you can add your own settings without worrying about commiting them.


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

### Development server

The dev server generates the tailwindcss file on template changes and triggers the client (browser page) to reload in order to apply the changes.

> **Note:** If the commands below fails, try starting a poetry shell first (`poetry shell`)

To run the backend in Dev mode run:

```bash
flask-livetw dev
```

### Build for production

Building for production in this case means to generate a minimized version of the tailwindcss file.

To build for production run:

```bash
flask-livetw build
```


<br/>

### Development Mail server

The development mail server is used to test the email functionality of the project when developing locally.

The suggested mail server is [NodemailerApp](https://nodemailer.com/app/).

Download and install the mail server.

Once installed, open the mail server and click on the "+" button.

Enter the name for the server, for example "service_search".

Once created go to "Local Server" and copy the information into the `.env` file:

```ini
# Flask-mail
MAIL_SERVER=
MAIL_PORT=
MAIL_USERNAME=
MAIL_PASSWORD=
```

> **Note:** The values above are the defaults, if you changed the values in the mail server, you must use the new values instead.

After adding the mail server information it can be started in the app on the "server" tab in the top menu using the "start server" button.


<br/>

## Project layout:

The backend is located in the `admin/` folder.

```text
🌳 admin/
┣ 📁 src/
┃ ┣ 📁 core/
┃ ┃ ┣ 📁 models/
┃ ┃ ┃ ┣ 📄 __init__.py
┃ ┃ ┃ ┣ 📄 base.py
┃ ┃ ┃ ┣ 📄 model_a.py
┃ ┃ ┃ ┣ 📄 model...
┃ ┃ ┃ ┗ 📄 util.py
┃ ┃ ┣ 📄 __init__.py
┃ ┃ ┣ 📄 bcrypt.py
┃ ┃ ┣ 📄 config.py
┃ ┃ ┣ 📄 csrf.py
┃ ┃ ┣ 📄 db.py
┃ ┃ ┗ 📄 seed.py
┃ ┣ 📁 services/
┃ ┃ ┣ 📄 __init__.py
┃ ┃ ┣ 📄 base.py
┃ ┃ ┣ 📄 service_a.py
┃ ┃ ┗ 📄 service...
┃ ┗ 📁 web/
┃   ┣ 📁 controllers/
┃   ┃ ┣ 📁 api/
┃   ┃ ┃ ┣ 📄 endpoint_a.py
┃   ┃ ┃ ┗ 📄 endpoint...
┃   ┃ ┣ 📄 __init__.py
┃   ┃ ┣ 📄 _helpers.py
┃   ┃ ┣ 📄 index.py
┃   ┃ ┣ 📄 page_a.py
┃   ┃ ┗ 📄 page...
┃   ┣ 📁 forms/
┃   ┃ ┃ 📄 form_a.py
┃   ┃ ┗ 📄 form...
┃   ┣ 📁 templates/
┃   ┃ ┣ 📁 _frags/
┃   ┃ ┃ ┣ 📄 flash_message.html
┃   ┃ ┃ ┗ 📄 fragment...
┃   ┃ ┣ 📁 _macros/
┃   ┃ ┃ ┣ 📄 form.html
┃   ┃ ┃ ┗ 📄 macro...
┃   ┃ ┣ 📁 admin/
┃   ┃ ┃ ┣ 📄 subroute_a.html
┃   ┃ ┃ ┗ 📄 subroute...
┃   ┃ ┣ 📄 base_layout.html
┃   ┃ ┣ 📄 error.html
┃   ┃ ┣ 📄 index.html
┃   ┃ ┣ 📄 layout.html
┃   ┃ ┗ 📄 maintenance.html
┃   ┗ 📄 __init__.py
┣ 📁 static/
┃ ┣ 📁 .dev/
┃ ┃ ┣ 📄 global.css
┃ ┃ ┣ 📄 live_reload.js
┃ ┃ ┗ 📄 tailwind.css
┃ ┣ 📁 js/
┃ ┃ ┗ 📄 layout.js
┃ ┗ 📄 tailwind_min.css
┣ 📄 .env
┣ 📄 .gitignore
┣ 📄 .pre-commit-config.yaml
┣ 📄 .python-version
┣ 📄 app.py
┣ 📄 compose.yaml
┣ 📄 poetry.lock
┣ 📄 poetry.toml
┣ 📄 pyproject.toml
┣ 📄 README.md
┗ 📄 tailwind.config.js
```

Folder and files description:

- `src/`: This folder contains the source code of the backend.
  - `core/`:
    This folder contains the models and utilities for the project.
  - `core/models/`:
    This folder contains the models for the project, the `base.py` file contains the base model class and the `util.py` file contains the utilities for working with the models.

    > **Note:** The `base.py` file contains the `BaseModel` class that is used as the base class for all the models in the project. This class is used to add common fields and methods to all the models.
  - `core/bcrypt.py`:
    This file contains the bcrypt setup for the project.
  - `core/config.py`:
    This file contains the configuration setup for the project.
  - `core/csrf.py`:
    This file contains the CSRF protection for the project.
  - `core/db.py`:
    This file contains the sqlalchemy database instance for the project.
  - `core/seed.py`:
    This file contains the seed function for all the models in the project.

    > **Note:** The seed function is used to create the initial data for the project. This function only can be called manually and must be called after the database is created.
  - `services/`:
    This folder contains the services for the project, the services are used to implement the business logic of the project.

    The `base.py` file contains the base service class and the `service_a.py` file contains the service for the `model_a.py` model.

    > **Note:** The service classes are used in the controllers to create, read, update and delete the models.
  - `web/`:
    This folder contains the controllers, forms and templates for the project.
  - `web/controllers/`:
    This folder contains the controllers (routes) for the project, the `api/` folder contains the api endpoints and the rest of the files contains the pages for the projects.

    > **Note:** The controllers are used to handle the requests and responses for the project.
  - `web/forms/`:
    This folder contains the forms for the project, the `form_a.py` file contains the forms related to the `model_a.py` model.

    > **Note:** The forms are used to create the html forms and validate the data from the requests.
  - `web/templates/`:
    This folder contains the templates for the project which maps to the controllers pages.
  - `web/templates/_frags/`:
    This folder contains the fragments for the project, the `flash_message.html` file contains the flash message fragment.

    > **Note:** The fragments are used to create reusable html code.
  - `web/templates/_macros/`:
    This folder contains the macros for the project, the `form.html` file contains the form macro.

    > **Note:** The macros are used to create customizable and reusable html code.
- `static/`:
  This folder contains the static files for the project.
  - `.dev/`:
    This folder contains the flask-livetw related files for the project.
  - `.dev/global.css`:
    This file contains the global css for the project.
  - `.dev/live_reload.js`:
    This file contains the javascript code for the live reload feature.
  - `.dev/tailwind.css`:
    This file contains the tailwindcss output css for the project.
  - `js/`:
    This folder contains the javascript files for the project.
  - `tailwind_min.css`:
    This file contains the minimized tailwindcss output css for production.

    > **Note:** This file must be generated manually with the `flask-livetw build` command.
- `.env`:
  This file contains the enviroment variables for the project (sentitive data).

  > **Note:** This file is not commited to the repository.
- `.gitignore`:
  This file contains the files/folders to be ignored by git.
- `.pre-commit-config.yaml`:
  This file contains the pre-commit configuration for the project. This configuration is used to run the linters and formatters before commiting the changes to the repository. This configuration is used to enforce the code style and format.

  For more information about pre-commit, see the [pre-commit documentation](https://pre-commit.com/).
- `.python-version`:
  This file contains the python version for the project (3.8.10) used by pyenv.
- `app.py`:
  This file contains the flask application instance for the project.
- `compose.yaml`:
  This file contains the docker compose configuration for the project. This configuration is used to run the database and pgadmin.
- `poetry.lock`:
  This file contains the poetry dependencies lock file.
- `poetry.toml`:
  This file contains the poetry especific configuration for the project.
- `pyproject.toml`:
  This file contains the poetry and tools configuration for the project.
- `README.md`:
  This file contains the project general information of the project backend.
- `tailwind.config.js`:
  This file contains the tailwindcss configuration for the project used in the templates.


<br/>

## Questions and Answers


### Which python version is used in the project?

The python version used in the project is `3.8.10`.


### Which python dependencies are used in the project?

The dependencies used in the project are listed in the [pyproject.toml](../admin/pyproject.toml) file under the `[tool.poetry.dependencies]` section.

The development dependencies are listed in the [pyproject.toml](../admin/pyproject.toml) file under the `[tool.poetry.dev-dependencies]` section.


### Where is the flask configuration?

The flask configuration is located in the [src/core/config.py](../admin/src/core/config.py) file.


### Where is tooling configuration?

The tooling configuration is located:

- pre-commit: [admin/.pre-commit-config.yaml](../admin/.pre-commit-config.yaml)
- pyenv: [admin/.python-version](../admin/.python-version)
- poetry: [admin/pyproject.toml](../admin/pyproject.toml)
- tailwindcss: [admin/tailwind.config.js](../admin/tailwind.config.js), [../admin/src/static/.dev/global.css](../admin/static/.dev/global.css) and [..admin/pyproject.toml](../admin/pyproject.toml) under the `[tool.flask-livetw]` section.


### Where is the database configuration?

The database configuration is located in the [admin/.env](../admin/.env) file.


### How to connect a postgress db from render?

First create a [render](https://dashboard.render.com/register) account.

Then go to dashboard.

Click on the "New" button and select "PostgresSQL".

Enter the following information:

- Name: `service_search` (`my_databases`or whatever you want)
- Database: `service_search` (`my_database` or whatever you want)
- Username: `dev` (`my_user` or whatever you want)
- Region: Default option its okay, no option availible in south america (Brazil)

Click on the "Create Database" button.

Once the database is created, click on the "Connect to this database" button.

From the connection string copy the following information:

- Host: `host`
- Port: `port`
- Username: `user`
- Password: `password`
- Database: `dbname`

> If `.env` file is not present, create it in the root of the project (where the `admin/` folder is located).

Add the following enviroment variables to the `.env` file:

```ini
# Postgres
DB_HOST=host
DB_PORT=port
DB_USER=user
DB_PASS=password
DB_NAME=dbname
```

> **Note:** The values above are the ones gathered from the connection string, if you update/regenerate the connection string, you must update the values in the `.env` file as well.

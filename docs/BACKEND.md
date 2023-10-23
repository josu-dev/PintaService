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
┣ 📄 Dockerfile
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
  - `Dockerfile`: This file contains the docker definition to run the project on a container.
  - `pyproject.toml`: This file contains the poetry and tools configuration for the project.
  - `tailwind.config.js`: This file contains the tailwindcss configuration for the project used in the templates.

> **Note:** A more detailed description of the files/folders can be found in the [Project layout](#project-layout) section.


<br />

## Table of contents:

- [Development enviroment](#development-enviroment)
  - [Pyenv](#pyenv)
  - [Poetry](#poetry)
  - [Enviroment variables](#enviroment-variables)
  - [Docker](#docker)
    - [Running the database and mail server](#running-the-database-and-mail-server)
    - [Runnig pgadmin](#runnig-pgadmin)
    - [Running the application](#running-the-application)
    - [Resetting the database](#resetting-the-database)
    - [Running all the services](#running-all-the-services)
    - [Stopping all the services](#stopping-all-the-services)
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

The enviroment variables are used to the tools and the application configuration.

All the enviroment variables are located in the [admin/.env.example](../admin/.env.example) file.

To start using the enviroment variables, copy the `.env.example` file to `.env`.

If the applicattion will be runned from the docker compose thats all the necessary configuration (all the defaults are fine).

If the application will be runned manually, the following enviroment variables must be added to the `.env` file:


```ini
# Postgres (docker compose)
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=username
DB_PASS=password
DB_NAME=pinta_service
```

The above variables and the defaults provided are planned to be used with docker compose, so if you aren't using it, you must change the values to match your custom configuration. In the [Questions and Answers](#questions-and-answers) section you can find more information about how to use different configurations.


<br/>

### Docker

Docker is the tool used to run the database, mail server and optionally pgadmin and the application itself.

To install docker, simple go to the [docker website](https://www.docker.com/) and follow the instructions.


#### Running the database and mail server

The database can be run using the docker compose file located in the root of the project (where the `admin/` folder is located).

To run the database, run the following command:

```bash
docker compose up -d
```

> **Note:** The `-d` flag is to detach the process from the terminal, so it can run in the background.

To access the mail server, open the browser and go to `http://localhost:9080` (or the port you configured).

Once you are in the mail server login page, enter the following information:

- **Username:** username
- **Password:** password

> **Note:** The values above are the defaults, if you changed the values in the enviroment variables, you must use the new values instead.


#### Runnig pgadmin

To run pgadmin, run the following command:

```bash
docker compose --profile pgadmin up -d
```

You can access the pgadmin using at `http://localhost:5050` (or the port you configured).

Once you are in the pgadmin login page, login using the credentials you configured in the enviroment variables.

To connect to the database, open pgAdmin and click on the "Add New Server" button.

Fill the form with the following information:

Initial panel:
- **Name:** pinta_service

Connection panel:
- **Host name/address:** db
- **Port:** 5432
- **Username:** username
- **Password:** password

Click on the "Save" button.

> **Note:** The values above are the defaults, if you changed the values in the enviroment variables, you must use the new values instead.

#### Running the application

To run the application, run the following command:

```bash
docker compose --profile backend up -d
```

You can access the application at `http://localhost:5001` (or the port you configured).


#### Resetting the database

To reset the database, run the following command:

```bash
flask reset-db
```

To seed the database, run the following command:

```bash
flask seed-db
```


#### Running all the services

To run all the services, run the following command:

```bash
docker compose --profile all up -d
```

#### Stopping all the services

To stop all the services, run the following command:

```bash
docker compose --profile all down
```


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
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.tabSize": 4
  },
  "black-formatter.args": [
    "--line-length=79",
  ],
  "editor.formatOnSave": true,
  "editor.tabSize": 2,
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

## Project layout

The backend is located in the `admin/` folder.

```text
🌳 admin/
┣ 📁 src/
┃ ┣ 📁 core/
┃ ┃ ┣ 📁 models/
┃ ┃ ┃ ┣ 📄 all_models.py
┃ ┃ ┃ ┣ 📄 base.py
┃ ┃ ┃ ┗ 📄 model...
┃ ┃ ┣ 📄 bcrypt.py
┃ ┃ ┣ 📄 config.py
┃ ┃ ┣ 📄 csrf.py
┃ ┃ ┣ 📄 db.py
┃ ┃ ┣ 📄 enums.py
┃ ┃ ┣ 📄 permissions.py
┃ ┃ ┣ 📄 seed.py
┃ ┃ ┗ 📄 test_data.py
┃ ┣ 📁 services/
┃ ┃ ┣ 📄 base.py
┃ ┃ ┗ 📄 service...
┃ ┣ 📁 utils/
┃ ┃ ┣ 📄 funcs.py
┃ ┃ ┗ 📄 status.py
┃ ┗ 📁 web/
┃   ┣ 📁 controllers/
┃   ┃ ┣ 📁 api/
┃   ┃ ┃ ┣ 📄 __init__.py
┃   ┃ ┃ ┣ 📄 base.py
┃   ┃ ┃ ┗ 📄 root...
┃   ┃ ┣ 📄 __init__.py
┃   ┃ ┣ 📄 _errors_.py
┃   ┃ ┣ 📄 _helpers.py
┃   ┃ ┗ 📄 routes...
┃   ┣ 📁 forms/
┃   ┃ ┗ 📄 form...
┃   ┣ 📁 templates/
┃   ┃ ┣ 📁 _errors/
┃   ┃ ┃ ┗ 📄 error...
┃   ┃ ┣ 📁 _frags/
┃   ┃ ┃ ┗ 📄 fragment...
┃   ┃ ┣ 📁 _layouts/
┃   ┃ ┃ ┗ 📄 fragment...
┃   ┃ ┣ 📁 _macros/
┃   ┃ ┃ ┗ 📄 macro...
┃   ┃ ┣ 📁 sub_route/
┃   ┃ ┃ ┗ 📄 page...
┃   ┃ ┣ 📄 index.html
┃   ┃ ┗ 📄 page...
┃   ┗ 📄 __init__.py
┣ 📁 static/
┃ ┣ 📁 .dev/
┃ ┃ ┣ 📄 global.css
┃ ┃ ┣ 📄 live_reload.js
┃ ┃ ┗ 📄 tailwind.css
┃ ┣ 📁 img/
┃ ┃ ┗ 📄 image...
┃ ┣ 📁 js/
┃ ┃ ┗ 📄 script...
┃ ┗ 📄 tailwind_min.css
┣ 📄 .env.example
┣ 📄 .gitignore
┣ 📄 .pre-commit-config.yaml
┣ 📄 .python-version
┣ 📄 app.py
┣ 📄 compose.yaml
┣ 📄 Dockerfile
┣ 📄 poetry.lock
┣ 📄 poetry.toml
┣ 📄 pyproject.toml
┣ 📄 README.md
┗ 📄 tailwind.config.js
```

Folder and files description:

- `src/`: This folder contains the source code of the backend.
  - `core/`:
    This folder contains the models and libraries for the project.
  - `core/models/`:
    This folder contains the models for the project, the `base.py` file contains the base model class for each model and the `all_models.py` file contains the imports for all the models in the project (to trigger the creation of the tables in the database).
  - `core/bcrypt.py`:
    This file contains the bcrypt setup to hash the passwords for the project.
  - `core/config.py`:
    This file contains the configuration module to load the enviroment variables for the project.
  - `core/csrf.py`:
    This file contains the CSRF protection for the project.
  - `core/db.py`:
    This file contains the sqlalchemy database instance for the project.
  - `core/enums.py`:
    This file contains the shared enums for the project.
  - `core/permissions.py`:
    This file contains the permissions definitions for the project.
  - `core/seed.py`:
    This file contains the seed function for the models that require initial data.
  - `core/test_data.py`:
    This file contains the test data for development.
  - `services/`:
    This folder contains the services for the project, the services are used to implement the business logic of the project.

    The `base.py` file contains the base service class and the `service_a.py` file contains the service for the `model_a.py` model.

    > **Note:** The service classes are used in the controllers to create, read, update and delete the models.
  - `utils/`:
    This folder contains the utilities for the project, the `funcs.py` file contains the utility functions and the `status.py` file contains the http status codes.
  - `web/`:
    This folder contains the routes defined in the controllers with the templates and forms used by the routes.
  - `web/controllers/`:
    This folder contains the controllers (routes) for the project, the `api/` folder contains the api endpoints and the rest of the files contains the pages for the projects.
  - `web/forms/`:
    This folder contains the forms for the project which maps to the controllers routes or groups of routes.

    > **Note:** The forms are used to create the html forms and validate the data from the requests.
  - `web/templates/`:
    This folder contains the templates used to create the html pages for the project.
  - `web/templates/_errors/`:
    This folder contains the error pages for the project, for example the `404.html` file contains the 404 error page.
  - `web/templates/_frags/`:
    This folder contains the fragments for the project, a fragment is a invariant reusable html code that can be used in multiple pages.
  - `web/templates/_layouts/`:
    This folder contains the layouts for the project, a layout is a html code that is used to wrap the content of a page with a common html code.
  - `web/templates/_macros/`:
    This folder contains the macros for the project, a macro is a customizable html code that can be used in multiple pages.
  - `web/__init__.py`:
    This file contains the flask application factory for the project.
- `static/`:
  This folder contains the static files for the project.
  - `.dev/`:
    This folder contains the flas-livetw files for development. The `global.css` file contains the global css for the project, the `live_reload.js` file contains the live reload script that triggers the browser to reload when the templates change and the `tailwind.css` file contains the tailwindcss output css generated from classes used in the templates.
  - `img/`:
    This folder contains the images for the project.
  - `js/`:
    This folder contains the scripts used in the templates.
  - `tailwind_min.css`:
    This file contains the minimized tailwindcss output css for production.

    > **Note:** This file must be generated manually with the `flask-livetw build` command.
- `.env.example`:
  This file contains the enviroment variables example for the project. This file is used as a template to create the `.env` file. The `.env` file contains the enviroment variables for the project (sentitive data) which never should be commited to the repository.
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
  This file contains the docker compose configuration for the project. This configuration is used to run the database and mail server for development. Optionally you can run the pgadmin and the aplicattion as well.
- `Dockerfile`:
  This file contains the docker image definition for the project. This configuration is used to run the application on a container.
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


### Where is the tooling configuration?

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


### How to connect a local mail server?

A local mail server is required to send emails during development without having to use a real email account or mail service.

This example uses [NodemailerApp](https://nodemailer.com/app/) as the mail server.

To install NodemailerApp, go to the website and download the version for your OS.

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

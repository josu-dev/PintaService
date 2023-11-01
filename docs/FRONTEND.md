# Frontend


This document describes the development enviroment, files/folders layout (structure) and tools used in the frontend of the project.

The backend is a [Vue.js](https://vuejs.org/) application with [Tailwindcss](https://tailwindcss.com/) as the css framework.

The node version used in the project is `v14.21.3`.

This document assumes that your working directory is the root of the project (where the `portal/` folder is located).

Some of the most important files/folders are:

```text
🌳 portal/
┣ 📁 public/
┣ 📁 src/
┣ 📄 .env
┣ 📄 .pre-commit-config.yaml
┣ 📄 app.py
┣ 📄 compose.yaml
┣ 📄 Dockerfile
┣ 📄 pyproject.toml
┗ 📄 tailwind.config.js
```

- `portal/`: This folder contains the backend of the project.
  - `

> **Note:** A more detailed description of the files/folders can be found in the [Project layout](#project-layout) section.


<br />

## Table of contents:

- [Development enviroment](#development-enviroment)
  - [nvm](#nvm)
  - [npm](#npm)
  - [Enviroment variables](#enviroment-variables)
  - [Docker](#docker)
    - [Running the backend](#running-the-database-and-mail-server)
    - [Running all the services](#running-all-the-services)
    - [Stopping all the services](#stopping-all-the-services)
  - [Editor setup (VSCode)](#editor-setup-vscode)
  - [husky](#husky)
  - [Development server](#development-server)
  - [Build for production](#build-for-production)
- [Project layout](#project-layout)
- [Questions and Answers](#questions-and-answers)


<br/>

## Development enviroment


<br/>

### Nvm (write this)

Pyenv is the tool used to manage the python versions for the project.

To install pyenv, follow the official [pyenv installation guide](https://github.com/pyenv/pyenv#installation).

After installing pyenv is recommended to run the following command to configure the virtual enviroments to be created inside the project folder

```bash
pyenv local 3.8.10
```


<br/>

### Node (write this)

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


#### Running the backend

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

- [name](url)


Its recommended to create a local settings file for the project at `.vscode/settings.json` or in `admin/.vscode/settings.json` if you want to open the project from the admin folder. Creating a local settings file allows you to customize the settings without affecting the global settings.

The settings are for the editor itself and the extensions.

Required settings:

```json
{
}
```

Optional settings:

```json
{
}
```

The .vscode folder is ignored by git, so you can add your own settings without worrying about commiting them.


<br/>

### husky

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
```

Folder and files description:

- `src/`: This folder contains the source code of the backend.
  - `

<br/>

## Questions and Answers


### ...

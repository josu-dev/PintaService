# Backend

This document describes the layout (folders and files structure) of the project backend.


<br/>

## Backend layout:

The backend is located in the `admin/` folder.

```text
🌳 admin/
┣ 📁 src/
┃ ┣ 📁 config/
┃ ┃ ┃ 📄 __init__.py
┃ ┃ ┗ 📄 config.py
┃ ┣ 📁 core/
┃ ┃ ┣ 📁 models/
┃ ┃ ┃ ┣ 📄 __init__.py
┃ ┃ ┃ ┣ 📄 base.py
┃ ┃ ┃ ┣ 📄 model_a.py
┃ ┃ ┃ ┣ 📄 model...
┃ ┃ ┃ ┗ 📄 util.py
┃ ┃ ┣ 📄 __init__.py
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
┃   ┃ ┣ 📄 index.py
┃   ┃ ┣ 📄 page_a.py
┃   ┃ ┗ 📄 page...
┃   ┣ 📁 forms/
┃   ┃ ┃ 📄 form_a.py
┃   ┃ ┗ 📄 form...
┃   ┣ 📁 templates/
┃   ┃ ┣ 📁 admin/
┃   ┃ ┃ ┗ 📄 site_config.html
┃   ┃ ┣ 📁 _macros/
┃   ┃ ┃ ┗ 📄 form.html
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


<br/>

## Folder src/

This folder contains the source code of the backend.

### src/config/

This folder contains the configurations for the project.

The sensitive configurations are loaded from the `.env` file located in the root of the project into the `config.py` file.


### src/core/

This folder contains the models and utilities for the project.

The `models/` folder contains the models for the project, the `base.py` file contains the base model class and the `util.py` file contains the utilities for working with the models.

> **Note:** The `base.py` file contains the `BaseModel` class that is used as the base class for all the models in the project. This class is used to add common fields and methods to all the models.

The `csrf.py` file contains the CSRF protection for the project.

The `db.py` file contains the sqlalchemy database instance for the project.

The `seed.py` file contains the seed function for all the models in the project.

> **Note:** The seed function is used to create the initial data for the project. This function only can be called manually and must be called after the database is created.


### src/services/

This folder contains the services for the project, the services are used to interact with the models.

The `base.py` file contains the base service class and the `service_a.py` file contains the service for the `model_a.py` model.

> **Note:** The service classes are used in the controllers to create, read, update and delete the models.


### src/web/

This folder contains the controllers, forms and templates for the project.

The `controllers/` folder contains the controllers (routes) for the project, the `api/` folder contains the api endpoints and the rest of the files contains the pages for the projects.

> **Note:** The controllers are used to handle the requests and responses for the project.

The `forms/` folder contains the forms for the project, the `form_a.py` file contains the forms related to the `model_a.py` model.

> **Note:** The forms are used to create the html forms and validate the data from the requests.

The `templates/` folder contains the templates for the project which maps to the controllers pages.


<br/>

## Folder static/

This folder contains the static files used in the controllers and templates.

### static/.dev/

This folder contains the flask-livetw related files. This files only are used in development time.

The `global.css` file contains the global css for the project.

The `live_reload.js` file contains the javascript code for the live reload feature.

The `tailwind.css` file contains the tailwindcss output css for the project.


### static/js/

This folder contains the javascript files used in the templates.


### static/tailwind_min.css

This file contains the minimized tailwindcss output css for production.

> **Note:** This file must be generated manually with the `flask-livetw build` command.


## Top level files

The root of the project contains the following files:

### .env

This file contains the enviroment variables for the project (sentitive data).

> **Note:** This file is not commited to the repository.


### .gitignore

This file contains the files/folders to be ignored by git.


### .pre-commit-config.yaml

This file contains the pre-commit configuration for the project. This configuration is used to run the linters and formatters before commiting the changes to the repository. This configuration is used to enforce the code style and format.

For more information about pre-commit, see the [pre-commit documentation](https://pre-commit.com/).


### .python-version

This file contains the python version for the project (3.8.10) used by pyenv.


### app.py

This file contains the flask application instance for the project.


### compose.yaml

This file contains the docker compose configuration for the project. This configuration is used to run the database and pgadmin.


### poetry.lock

This file contains the poetry dependencies lock file.


### poetry.toml

This file contains the poetry especific configuration for the project.


### pyproject.toml

This file contains the poetry and tools configuration for the project.


### README.md

This file contains the project general information of the project backend.


### tailwind.config.js

This file contains the tailwindcss configuration for the project used in the templates.

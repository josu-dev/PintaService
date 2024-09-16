# Frontend


This document describes the development enviroment, files/folders layout (structure) and tools used in the public frontend application of the project.

The public frontend is a [Vue.js](https://vuejs.org/) application with [Tailwindcss](https://tailwindcss.com/) as the css framework.

The node version used in the project is `v22.8.0`.

This document assumes that your working directory is `portal/` (the folder for the public frontend).

Some of the most important files/folders are:

```text
🌳 portal/
┣ 📁 public/
┣ 📁 src/
┣ 📄 compose.yaml
┣ 📄 Dockerfile
┣ 📄 index.html
┣ 📄 package.json
┣ 📄 tailwind.config.js
┗ 📄 vite.config.js
```

- `portal/`: This folder contains the backend of the project.
  - `public/`: This folder contains the static files of the project.
  - `src/`: This folder contains the source code of the backend.
  - `compose.yaml`: This file contains the docker compose definition to run the frontend.
  - `Dockerfile`: This file contains the docker definition to build the frontend image.
  - `index.html`: This file is the entry point of the frontend where the vue application is mounted.
  - `package.json`: This file contains the node dependencies and scripts for the project.
  - `tailwind.config.js`: This file contains the tailwindcss configuration.
  - `vite.config.js`: This file contains the vite configuration, which is the tool to develop and build the vue application.

> **Note:** A more detailed description of the files/folders can be found in the [Project layout](#project-layout) section.


<br />

## Table of contents:

- [Development enviroment](#development-enviroment)
  - [nvm](#nvm)
  - [Enviroment variables](#enviroment-variables)
  - [Docker](#docker)
    - [Running the backend](#running-the-database-and-mail-server)
    - [Running all the services](#running-all-the-services)
    - [Stopping all the services](#stopping-all-the-services)
  - [Editor setup (VSCode)](#editor-setup-vscode)
  - [Development server](#development-server)
  - [Build for production](#build-for-production)
- [Project layout](#project-layout)
- [Questions and Answers](#questions-and-answers)


<br/>

## Development enviroment


### nvm

nvm is the tool used to manage the node versions for the project.

To install nvm, follow the official [nmv installation guide](https://github.com/nvm-sh/nvm#installing-and-updating).

> If you are using windows, you can use [nvm-windows](https://github.com/coreybutler/nvm-windows) instead.

After installing nvm, run the following command to install the node version used in the project:

```bash
nvm install 22.8.0
```

To use the node version installed, run the following command:

```bash
nvm use 22.8.0
```


### Enviroment variables

The enviroment variables are used to the tools and the application configuration.

All the enviroment variables are located in the [portal/.env.example](../portal/.env.example) file.

To start using the enviroment variables, copy the `.env.example` file to `.env`.

If the applicattion will be runned from the docker compose thats all the necessary configuration (all the defaults are fine).

If the application will be runned manually, the following enviroment variables must be added to the `.env` file:


```ini
# Base URL for the backend API
VITE_BACKEND_BASE_URL=http://127.0.0.1:5000
```

The above variables and the defaults provided are planned to be used with docker compose, so if you aren't using it, you must change the values to match your custom configuration.


### Docker

Docker is the tool used to easy run the necessary services for the project (database, mail server, etc). Optionally, it can be used to run the backend and the frontend for development.

> The guide for running the backend and services with docker compose can be found in the [backend documentation](../admin/README.md).

To install docker, simple go to the [docker website](https://www.docker.com/) and follow the instructions.


#### Running the vue application

To run the vue application, run the following command:

```bash
docker compose up -d
```

> **Note:** The `-d` flag is to detach the process from the terminal, so it can run in the background.

To access the vue application, go to [localhost:4174](http://localhost:4174) (or the port you configured) in your browser.


#### Stopping the vue application

To stop the vue application, run the following command:

```bash
docker compose down
```


### Editor setup (VSCode)

Recommended extensions:

- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [Volar](https://marketplace.visualstudio.com/items?itemName=vue.volar)


Its recommended to create a local settings file for the project at `.vscode/settings.json` or in `portal/.vscode/settings.json` if you want to open the project from the portal folder.

> Creating a local settings file allows you to customize the settings without affecting the global settings.

The settings are for the editor itself and the extensions.

Required settings:

```json
{
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.formatOnSave": true,
  "editor.tabSize": 2,
  "prettier.useTabs": false,
  "prettier.tabWidth": 2,
  "prettier.vueIndentScriptAndStyle": true
}
```

The .vscode folder is ignored by git, so you can add your own settings without worrying about commiting them.


### Development server

The dev server is used to serve the vue application in development mode, meaning that it will automatically reload the page when a file is changed.

To run the dev server, run the following command:

```bash
npm run dev
```

> If the command fails, make sure that you are using the correct node version (see [nvm](#nvm)).


### Build for production

The build command is used to build the vue application for production, meaning that it will prepare the application to be served by a web server, making the necessary optimizations.

To run the build command, run the following command:

```bash
npm run build
```

> If the command fails, make sure that you are using the correct node version (see [nvm](#nvm)).

The build files will be located in the `dist/` folder.

To locally see the builded application, run the following command:

```bash
npm run preview
```


<br/>

## Project layout

The public frontent is located in the `portal/` folder.

```text
🌳 portal/
┣ 📁 public/
┃ ┗ 📄 images...
┣ 📁 src/
┃ ┣ 📁 assets/
┃ ┣ 📁 components/
┃ ┣ 📁 router/
┃ ┣ 📁 stores/
┃ ┣ 📁 views/
┃ ┣ 📄 App.vue
┃ ┗ 📄 main.js
┣ 📄 .env.example
┣ 📄 .eslintignore
┣ 📄 .eslintrc.cjs
┣ 📄 .gitignore
┣ 📄 .prettierignore
┣ 📄 .prettierrc.json
┣ 📄 compose.yaml
┣ 📄 Dockerfile
┣ 📄 index.html
┣ 📄 package-lock.json
┣ 📄 package.json
┣ 📄 postcss.config.cjs
┣ 📄 README.md
┣ 📄 tailwind.config.cjs
┗ 📄 vite.config.js
```

Folder and files description:

- `public/`:
  This folder contains the static files of the project.
- `src/`:
  This folder contains the source code of the backend.
  - `assets/`:
    This folder contains the assets of the project (images, fonts, etc).
  - `components/`:
    This folder contains the vue components used to compose the views.
  - `router/`:
    This folder contains the [vue router](https://router.vuejs.org/) configuration.
  - `stores/`:
    This folder contains the [pinia](https://pinia.vuejs.org/) stores used to manage the application state.
  - `views/`:
    This folder contains the vue components used as views.
  - `App.vue`:
    This file is the root vue component of the application.
  - `main.js`:
    This file is the entry point of the application.
- `.env.example`:
  This file contains the enviroment variables used in the project.
- `.eslintignore`:
  This file contains the files/folders to ignore for the eslint linter.
- `.eslintrc.cjs`:
  This file contains the eslint configuration.
- `.gitignore`:
  This file contains the files/folders to ignore for git.
- `.prettierignore`:
  This file contains the files/folders to ignore for the prettier formatter.
- `.prettierrc.json`:
  This file contains the prettier configuration.
- `compose.yaml`:
  This file contains the docker compose definition to run the frontend.
- `Dockerfile`:
  This file contains the docker definition to build the frontend image.
- `index.html`:
  This file is the entry point of the frontend where the vue application is mounted.
- `package-lock.json`:
  This file contains the especific versions of the node dependencies.
- `package.json`:
  This file contains the node dependencies and scripts for the project.
- `postcss.config.cjs`:
  This file contains the postcss configuration.
- `README.md`:
  This file contains the project general information of the project backend.
- `tailwind.config.cjs`:
  This file contains the tailwindcss configuration.


<br/>

## Questions and Answers

### What is vite?

Vite is a framework for building frontend applications, it is used to develop and build the vue application.

For more information, go to the [vite website](https://vitejs.dev/).

### What is DaisyUI?

DaisyUI is a component library for tailwindcss, it is used to create the UI of the application.

For more information, go to the [DaisyUI website](https://daisyui.com/).

# Grupo 04

Proyecto para la materia de **Proyecto de Software 2023** de la [Facultad de Informática UNLP](https://www.info.unlp.edu.ar/).

El objetivo de este proyecto es desarrollar un sistema que permita registrar y gestionar los servicios ofrecidos por las instituciones o centros de Investigación y Desarrollo en Tecnología de Pinturas. Estos centros contarán con un conjunto de características como nombre, descripción, contacto, entre otras. Para lo cual se desarrollaron dos aplicaciones, una privada para la administración de los centros y otra pública para que los clientes puedan acceder a la información de los mismos.


## Aplicacion privada

Esta aplicación sera utilizada tanto por los administradores del sistema que tienen el acceso a la administración de los usuarios y también por usuarios asociados a cada una de las instituciones para que puedan administrar las mismas agregando los servicios que ofrecen

La aplicacion se encuentra desplegada en [https://admin-grupo04.proyecto2023.linti.unlp.edu.ar](https://admin-grupo04.proyecto2023.linti.unlp.edu.ar/)

El codigo fuente se encuentra en la carpeta [./admin](./admin)

> Para mas información sobre la aplicación privada, ver el [README.md](./admin/README.md) de la misma


## Aplicacion publica

Esta aplicación sera con la cual accederan tanto los clientes para obtener información de interés sobre el Laboratorio, información Institucional y servicios habilitados, como los administradores para revisar las estadisticas de todas las instituciones.

La aplicacion se encuentra desplegada en [https://grupo04.proyecto2023.linti.unlp.edu.ar](https://grupo04.proyecto2023.linti.unlp.edu.ar/)

El codigo fuente se encuentra en la carpeta [./portal](./portal)

> Para mas información sobre la aplicación publica, ver el [README.md](./portal/README.md) de la misma


## Credenciales de acceso

Credenciales de acceso para las aplicaciones desplegadas en producción:

| Usuario               | Contraseña               | Rol                 |
| --------------------- | ------------------------ | ------------------- |
| admin@catedras.com    | admincatedraspassword    | Super Administrador |
| duenio@catedras.com   | dueniocatedraspassword   | Dueño               |
| manager@catedras.com  | managercatedraspassword  | Administrador       |
| operador@catedras.com | operadorcatedraspassword | Operador            |
| sinrol@catedras.com   | sinrolcatedraspassword   |                     |

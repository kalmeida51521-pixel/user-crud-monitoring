# CRUD de Usuarios con FastAPI, PostgreSQL, Prometheus y Grafana

## Descripción
Este proyecto implementa una API REST para la gestión de usuarios utilizando FastAPI y PostgreSQL.

La aplicación permite realizar las operaciones CRUD (Crear, Leer, Actualizar y Eliminar usuarios) y cuenta con un sistema de monitoreo utilizando Prometheus y Grafana.

Todos los servicios se ejecutan mediante Docker y Docker Compose.

## Tecnologías utilizadas
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- Prometheus
- Grafana

## Arquitectura del proyecto
El proyecto está compuesto por cuatro servicios principales:

- **FastAPI:** API REST para gestionar los usuarios.
- **PostgreSQL:** Base de datos para almacenar los usuarios.
- **Prometheus:** Recolección de métricas de la API.
- **Grafana:** Visualización de las métricas obtenidas por Prometheus.

Flujo general:

FastAPI → PostgreSQL

FastAPI → Prometheus → Grafana

## Estructura del proyecto

```text
user-crud-monitoring/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── prometheus/
│   └── prometheus.yml
│
├── docker-compose.yml
└── README.md
```

## CRUD de usuarios

La API permite realizar las siguientes operaciones:

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/users` | Obtener todos los usuarios |
| GET | `/users/{user_id}` | Obtener un usuario por ID |
| POST | `/users` | Crear un usuario |
| PUT | `/users/{user_id}` | Actualizar un usuario |
| DELETE | `/users/{user_id}` | Eliminar un usuario |
| GET | `/metrics` | Exponer métricas para Prometheus |

## Base de datos

El proyecto utiliza PostgreSQL como sistema de gestión de base de datos.

La API se conecta a PostgreSQL mediante SQLAlchemy.

Los datos principales almacenados para cada usuario son:

- ID
- Nombre
- Edad

## Métricas con Prometheus

La API expone sus métricas mediante el endpoint:

```text
/metrics
```

Se implementó la métrica personalizada:

```text
user_created_total
```

Esta métrica registra el número de usuarios creados mediante la API.

Prometheus obtiene las métricas directamente desde el servicio FastAPI.

## Dashboard de Grafana

Grafana utiliza Prometheus como fuente de datos.

La conexión utilizada entre los contenedores es:

```text
http://prometheus:9090
```

El dashboard implementado contiene los siguientes paneles:

### Total de usuarios creados

Muestra mediante una visualización tipo **Stat** la cantidad total registrada por:

```text
user_created_total
```

### Evolución de usuarios creados

Muestra mediante una gráfica **Time series** la evolución de la métrica:

```text
user_created_total
```

## Ejecución del proyecto

### Requisitos

Es necesario tener instalados:

- Docker
- Docker Compose

### Iniciar los servicios

Desde la raíz del proyecto ejecutar:

```bash
docker compose up --build
```

También se pueden iniciar en segundo plano:

```bash
docker compose up -d --build
```

### Verificar los contenedores

```bash
docker compose ps
```

Los servicios esperados son:

```text
fastapi_app
postgres_container
prometheus
grafana
```

## Acceso a los servicios

Una vez iniciados los contenedores:

### FastAPI / Swagger

```text
http://localhost:8000/docs
```

Desde Swagger se pueden probar las operaciones CRUD.

### Métricas de FastAPI

```text
http://localhost:8000/metrics
```

### Prometheus

```text
http://localhost:9090
```

La métrica personalizada se puede consultar utilizando:

```text
user_created_total
```

### Grafana

```text
http://localhost:3000
```

Grafana está conectado a Prometheus para visualizar las métricas de la aplicación.

## Detener el proyecto

Para detener los contenedores:

```bash
docker compose down
```

## Conclusión

Este proyecto demuestra la construcción de una API REST utilizando FastAPI y PostgreSQL, ejecutada mediante contenedores Docker.

Además, se implementó monitoreo mediante Prometheus y visualización de métricas mediante Grafana, permitiendo observar el comportamiento de la aplicación y el número de usuarios creados.

El proyecto integra desarrollo de API, persistencia de datos, contenerización y monitoreo en una misma arquitectura.
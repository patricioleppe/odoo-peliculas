# Módulo de Gestión de Películas en Odoo

Este módulo personalizado para Odoo integra la consulta de un servicio externo de películas mediante REST API, registra la información en un modelo propio y expone un endpoint REST para obtener el top 10 de películas según su ranking.

## Características

- Consulta automática cada minuto a la API externa de películas
- Almacenamiento de películas con su título y ranking
- Interfaz de usuario para gestionar los registros de películas
- Endpoint REST para obtener el top 10 de películas por ranking

## Requisitos

- Docker y Docker Compose instalados
- Git

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/movie-management.git
   cd movie-management
   ```

2. Iniciar los contenedores con Docker Compose:
   ```
   docker-compose up -d
   ```

3. Acceder a Odoo:
   - URL: http://localhost:8069
   - Crear una base de datos
   - Instalar el módulo "Gestión de Películas" desde la lista de aplicaciones

## Configuración

1. Verificar los parámetros del sistema:
   - Ir a Ajustes > Parámetros > Parámetros del sistema
   - Verificar que existan los parámetros:
     - `movie_management.api_url`: URL de la API (por defecto: https://random-data-api.com/api/v3/projects/a2bebcc5-69e3-4b4e-b8c0-4a2f4306f0da)
     - `movie_management.api_key`: Clave de API (por defecto: ZN-BE0NeUFPRYdYrRZf7CQ)

## Uso

### Interfaz de Usuario
- Acceder al menú "Gestión de Películas" > "Películas" para ver los registros almacenados

### Cron Job
- El sistema consultará automáticamente la API cada minuto
- Los registros de ejecución pueden verse en Ajustes > Técnico > Automatización > Acciones planificadas

### Endpoint REST
- Para obtener el top 10 de películas, realizar una petición GET a:
  ```
  http://localhost:8069/api/top_movies
  ```
- El resultado será un JSON con los IDs, títulos y rankings de las películas

## Pruebas

### Verificar funcionamiento del Cron
1. Esperar un minuto después de instalar el módulo
2. Verificar en el menú de películas si se han creado nuevos registros

### Verificar funcionamiento del Endpoint
1. Asegurarse de que existen películas en el sistema
2. Realizar una petición GET al endpoint usando curl o un navegador:
   ```
   curl http://localhost:8069/api/top_movies
   ```

## Estructura del Proyecto

```
movie_management/
├── __init__.py                  # Inicialización del módulo
├── __manifest__.py              # Manifiesto y metadata
├── controllers/                 # Controladores REST
│   ├── __init__.py
│   └── main.py                  # Endpoint de top películas
├── data/
│   └── cron.xml                 # Definición del cron job
├── models/
│   ├── __init__.py
│   └── movie.py                 # Modelo de películas
├── security/
│   └── ir.model.access.csv      # Reglas de acceso
└── views/
    └── movie_view.xml           # Vistas UI y parámetros del sistema
docker-compose.yml               # Configuración para despliegue
```

## Desarrollo

Este proyecto sigue la metodología GitFlow con las siguientes ramas:
- `main`: Código en producción
- `develop`: Código en desarrollo
- `feature/xxx`: Nuevas funcionalidades
- `hotfix/xxx`: Correcciones urgentes

## Licencia

Este proyecto está bajo la licencia [LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.html), consistente con la licencia de Odoo Community.
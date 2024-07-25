# Backend Documentation

The backend was developed using the FastAPI framework in Python.

## Architecture

The project follows a Models-Views-Controller-Services (MVCS) architecture to enhance the developer experience and facilitate easier and more understandable development within the codebase.

### Models

The database tables and columns are represented in the `/app/models/models.py` file through appropriate classes. These models enable easy data parsing in the backend.

### Schemas

Since FastAPI is used in this project, schemas are implemented instead of views. Schemas for the relevant tables are located in the `/app/schemas` directory. These schemas are used for data validation and serialization/deserialization, making it easier to structure returned JSONs in the FastAPI application.

### Controller

Endpoints for both requests and user calls are defined in the `/app/controller` directory. JWT tokens are also validated here. In these files, endpoints are organized as RESTful, and service functions are called to handle the necessary responses.

### Services

The `/app/services` folder contains all services, separated according to the tables or jobs they serve, following best practices. This includes service functions for blockchain communication, JWT token creation, and execution and return of necessary database queries.

### DB Folder

- `db.sql`: Contains queries to create mock data for the project in the database. PostgreSQL is used as the database provider.
- `postgres.py`: Sets up the database server.
- `initialise_db.py`: Establishes the connection with the installed server and checks if the database is already installed. If not, it runs the `db_create.py` file to ensure its installation, allowing the execution of SQL queries in `db.sql`. This ensures a local database installation is always available for the developer.
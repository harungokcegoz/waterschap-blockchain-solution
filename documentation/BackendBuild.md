# Backend Build

The backend is built using `FastAPI`. Due to the many dependencies required, `backendBuild.sh` was created to simplify the build process.

## Build Process

### `backendBuild.sh`

- Detects whether the operating system is macOS or Windows.
- Runs `build.py` with the necessary command for the detected OS.


#### `build.py`:
  - Manually added dependencies are installed first.
  - Dependencies specified in `requirements.txt` are installed automatically.

- ### Database Initialization

- Runs `app/db/initialise_db.py` to create the local database and mock data. Detailed info about database creation steps are available in `BackendStructure.md`.

- ### Running FastAPI

- As a final step to get everything worked, `app/main.py` runs FastAPI(Backend).

## Running the Backend

To run all these steps with a single command:

1. Navigate to the directory where `backendBuild.sh` is located.
2. Run the following command:

```bash
bash backendBuild.sh
```

Ensure that the Postgres server is running on your computer. If it is, the entire backend and database will operate smoothly.


#### `Note: If changes are made to db.sql, the queries must be re-executed. This requires deleting the existing database on the Postgres server and running backendBuild.sh again. Failure to do this will result in the changes not being applied.`
# Rihal Data Engineering Challenge

Welcome to the Rihal Data Engineering Challenge! Follow the instructions below to set up and explore the project.

## Prerequisites
- Ensure **Docker** is installed on your system.
- Verify that the following ports are **not in use**: `3000`, `8000`, `5050`, `5432`.

## Setup Instructions
1. **Start the Application**
   - In the root directory, run the following command:
    ```
    ./start.sh
    ```

- This will build and start four containers:
- `psql` (PostgreSQL database)
- `pgadmin` (Database management tool)
- `api` (Backend API)
- `web` (Frontend web application)
- Note: The initial build may take some time.

2. **Wait for API Confirmation**
- Monitor the logs for the `api` container.
- Wait until you see the message: **"Application has started successfully"** before proceeding to the web app(it might take some time since it is downloading `microsoft/trocr-base-handwritten`).

## Accessing the Application
- **Web Application**
- Once the API is running, access the web app at: `http://localhost:3000`
- The web app displays answers to the challenge questions using data fetched via SQL queries.

- **pgAdmin (Database Management)**
- Open your browser and go to: `http://localhost:5050`
- Log in with the following credentials:
    - **Email**: `admin@rihal.com`
    - **Password**: `admin`
- Register a server to connect to the PostgreSQL database:
- **Host**: `db`
- **Username**: `rihal_user`
- **Password**: `rihal_pwd`

- **Database Details**
- Database name: `rihal_db`
- Table: `crime_data`

## Challenge Notes
- The web app on port `3000` showcases answers to the challenge questions, derived purely from SQL queries.
- While further visualization was considered, the current implementation focuses on raw SQL output due to time and interest constraints.
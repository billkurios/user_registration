# User Registration API

A FastAPI-based user registration service.

## Prerequisites

- Docker
- Python 3.12 (optional, for local development)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd user_registration
   ```

2. If running locally without Docker:
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## Running the Application

### Using Docker (Recommended)

There are two images: the FastAPI application and a PostgreSQL database. They are defined in `docker-compose.yml`.

1. Start both services with Docker Compose:
   ```bash
   docker-compose up --build
   ```

   This will build the `web` image from the `Dockerfile` and pull the official Postgres image.

2. The web service depends on the `db` service and will use the following connection string by default:
   ```text
   postgresql://postgres:password@db:5432/userdb
   ```

3. Access the API at `http://localhost:8000` once the containers are running.

You can also still build the web image alone if desired:

```bash
# build only the application image
docker build -t fastapi-app .

# run the app without the database
docker run -p 8000:8000 fastapi-app
```

### Local Development

1. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Access the API at `http://localhost:8000`

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for the interactive API documentation provided by Swagger UI.

## License

This project is licensed under the terms specified in the LICENSE file.
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

1. Build the Docker image:
   ```bash
   docker build -t fastapi-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 fastapi-app
   ```

3. Access the API at `http://localhost:8000`

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
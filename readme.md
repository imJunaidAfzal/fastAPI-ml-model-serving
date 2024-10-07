# FastAPI ML Model Serving API

## Overview

This FastAPI application serves a machine learning model and is designed to handle large traffic loads efficiently. The application is built with scalability in mind, featuring:

- **Asynchronous request handling** to serve multiple clients concurrently.
- **In-memory caching** to reduce redundant model inference calls.
- **Health check endpoint** for easy monitoring.

You can easily integrate any machine learning model for inference by modifying the `model.py` file.

## Features

- **Asynchronous API**: Non-blocking I/O with `async`/`await` for better concurrency.
- **Cache Layer**: Simple in-memory cache to store results for a configurable amount of time.
- **Easy Scalability**: Designed for use with Uvicorn, allowing multi-worker deployment for high traffic scenarios.

Here’s the updated **Installation** section to include steps for creating and activating a virtual environment before installing dependencies:

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/imJunaidAfzal/fastAPI-ml-model-serving.git
    cd fastAPI-ml-model-serving
    ```

2. Create and activate a Python virtual environment:

    On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. Install the required dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

4. AUTH-KEY setup
    - Create `.env` file and set `AUTH_KEY="your_auth_key"`

5. Run the API:

    ```bash
    python -m uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
    ```

### Explanation:

- The virtual environment (`venv`) is created and activated before installing dependencies to ensure isolated package management.
- The `requirements.txt` file is used to install all the necessary dependencies.

## Usage

### 1. Predict Endpoint

- **URL**: `/predict/`
- **Method**: `POST`
- **Payload**:

    ```json
    {
        "text": "your input text"
    }
    ```

- **Response**:

    ```json
    {
        "result": "Processed text: your input text"
    }
    ```

### 2. Health Check

- **URL**: `/health/`
- **Method**: `GET`
- **Response**:

    ```json
    {
        "status": "ok"
    }
    ```

## Docker setup

1. Build the Docker image:

    ```bash
    docker build -t fastapi-ml-api .  
    ```

2. Run the Docker container:

    ```bash
    docker run -p 8000:8000 fastapi-ml-api
    ```

## Scaling and Performance

- **Asynchronous Design**: The API is fully asynchronous, which allows it to handle multiple requests without blocking.
- **Caching**: The cache stores the results of previous predictions for 500 seconds, reducing the load on the model.
- **Multi-worker Setup**: The app can be scaled horizontally using multiple workers. You can adjust the number of workers depending on your hardware and traffic load:

    ```bash
    python -m uvicorn app:app --workers 4
    ```

    Increase or decrease the number of workers based on your traffic requirements.


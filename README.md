# URL Shortener Service

This project is a scalable URL shortener service implemented with FastAPI, Docker, and integrated with Prometheus and Grafana for monitoring. The setup includes load balancing using Nginx.

## Table of Contents

- [URL Shortener Service](#url-shortener-service)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Build and Run the Services](#2-build-and-run-the-services)
  - [Project Structure](#project-structure)
  - [Services Overview](#services-overview)
  - [Stress Testing](#stress-testing)
    - [Using Locust](#using-locust)
    - [Using Wrk](#using-wrk)
  - [Monitoring with Prometheus and Grafana](#monitoring-with-prometheus-and-grafana)
  - [Diagram](#diagram)

## Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- `pip` (Python package installer)

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

### 2. Build and Run the Services

Ensure you have Docker and Docker Compose installed. Run the following command to build and start the services:

```sh
docker-compose up --scale web=3 --build
```

This command will start all services, including the database, cache, web servers, Nginx load balancer, Prometheus, Grafana, and Node Exporter.

## Project Structure

```plaintext
url-shortener/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── crud.py
├── migrations/
│   └── versions/
├── tests/
│   └── test_app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── nginx.conf
└── README.md
```

## Services Overview

- **web**: FastAPI application for URL shortening and redirection.
- **db**: PostgreSQL database to store URL mappings.
- **cache**: Redis cache for faster URL lookups.
- **nginx**: Nginx load balancer to distribute requests across multiple web service instances.
- **prometheus**: Prometheus for collecting metrics.
- **grafana**: Grafana for visualizing metrics.
- **node_exporter**: Node Exporter for system metrics.

## Stress Testing

### Using Locust

1. Install Locust:

    ```sh
    pip install locust
    ```

2. Create a `locustfile.py`:

    ```python
    from locust import HttpUser, task, between, constant
    from faker import Faker

    fake = Faker()

    class URLShortenerUser(HttpUser):
        wait_time = constant(1)

        @task(2)
        def shorten_url(self):
            original_url = fake.url()
            self.client.post("/shorten", json={"original_url": original_url})

        @task(1)
        def redirect_url(self):
            self.client.get("/6h61zg")  # Replace with a valid short URL from your service
    ```

3. Run Locust:

    ```sh
    locust -f locustfile.py --host http://localhost:8000
    ```

4. Open the Locust web interface at `http://localhost:8089` to start the test.

### Using Wrk

1. Install Wrk:

    ```sh
    brew install wrk  # On macOS
    ```

2. Create a `post.lua` script:

    ```lua
    local counter = 0
    local urls = {
        "https://example.com",
        "https://example.org",
        "https://example.net",
        "https://example.edu",
        "https://example.gov",
        "https://example.io",
        "https://example.co"
    }

    function request()
        local url = urls[counter % #urls + 1]
        counter = counter + 1

        wrk.method = "POST"
        wrk.body = string.format('{"original_url": "%s"}', url)
        wrk.headers["Content-Type"] = "application/json"

        return wrk.format(nil, "/shorten")
    end
    ```

3. Run Wrk:

    ```sh
    wrk -t12 -c400 -d30m --rate 555 http://localhost:8000/shorten -s post.lua
    ```

## Monitoring with Prometheus and Grafana

1. Access Prometheus at `http://localhost:9090`.
2. Access Grafana at `http://localhost:3000` (default login: `admin/admin`).

### Import Dashboards

1. **Prometheus 2.0 Overview**: Dashboard ID `3662`
2. **Node Exporter Full**: Dashboard ID `1860`


By following these instructions, you can set up, run, and monitor a scalable URL shortener service using Docker, Nginx, FastAPI, PostgreSQL, Redis, Prometheus, and Grafana.
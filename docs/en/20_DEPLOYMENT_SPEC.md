# Deployment & Infrastructure Specification

## 1. Overview
This document defines the container deployment strategy targeting Google Cloud Run (Serverless).
It utilizes a **Dual Service Model** to separate **API Service** and **Admin Service** within a **Monorepo** structure, and applies differentiated build strategies for **Development (Dev)** and **Production (Prod)** environments.

---

## 2. Architecture

### 2.1. Dual Service Model
To overcome the single-port limitation of serverless environments (1 Container = 1 Port) and maximize efficiency, the application is deployed as two independent services.

| Service Name (Example) | Role | Entrypoint Command | URL (Example) |
|---|---|---|---|
| **API Service** | REST API Provider (FastAPI) | `uvicorn main:app` | `https://api.example.com` |
| **Admin Service** | Admin UI Provider (Streamlit) | `streamlit run admin.py` | `https://admin.example.com` |

---

## 3. Docker Build Strategy

### 3.1. Multi-stage Build
Uses `ARG` and `Target` within a single `Dockerfile` to generate environment-specific images.

- **Base**: Common OS and Python package installation.
- **Development (Dev)**: Mounts source code, enables hot-reloading, includes debugging tools.
- **Production (Prod)**: Copies source code (Immutable), optimized, security-focused.

### 3.2. Dockerfile Specification Example
```dockerfile
# 1. Base Stage
FROM python:3.10-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Development Stage (Target: dev)
FROM base as dev
# Source code is mounted via volume, not copied
ENV PYTHONPATH=/app/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

# 3. Production Stage (Target: prod)
FROM base as prod
# Source code is definitively copied into the image
COPY . .
ENV PYTHONPATH=/app/src
# Entrypoint is overridden at deployment time
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 4. Deployment Guide

### 4.1. Development
Uses local volume mounts or dev containers for rapid iteration.
- **Build Command**: `docker build --target dev -t myapp:dev .`
- **Features**: Changes are reflected immediately (Hot-reload).

### 4.2. Production
Builds and deploys an image containing the source code for stability and immutability.
- **Build Command**: `docker build --target prod -t myapp:prod .`
- **Cloud Run Deploy**:
    ```bash
    # Deploy API Service
    gcloud run deploy llm-api --image myapp:prod --command "uvicorn" --args "main:app" ...
    
    # Deploy Admin Service
    gcloud run deploy llm-admin --image myapp:prod --command "streamlit" --args "run,streamlit/admin.py" ...
    ```

---

## 5. Cost Optimization

### 5.1. Scale to Zero
Leverages Cloud Run's "Scale to Zero" capability by default.
- **Setting**: `min-instances: 0` (Default)
- **Effect**: Keeps costs near **$0** for intermittently used services like the Admin Console.


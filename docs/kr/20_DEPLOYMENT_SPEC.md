# 배포 및 인프라 명세 (Deployment & Infrastructure Spec)

## 1. 개요 (Overview)
본 문서는 Google Cloud Run(Serverless) 환경을 타겟으로 하는 컨테이너 배포 전략을 정의합니다.
**단일 리포지토리(Monorepo)** 구조에서 **API 서비스**와 **Admin 서비스**를 분리하여 배포하며, **개발계(Development)**와 **운영계(Production)** 환경에 따라 차별화된 빌드 전략을 사용합니다.

---

## 2. 아키텍처 (Architecture)

### 2.1. 서비스 분리 모델 (Dual Service Model)
서버리스 환경의 포트 제약(1 Container = 1 Port)을 극복하고 효율성을 높이기 위해 두 개의 독립된 서비스로 배포합니다.

| 서비스명 (예시) | 역할 | 실행 명령 (Entrypoint) | URL (예시) |
|---|---|---|---|
| **API Service** | REST API 제공 (FastAPI) | `uvicorn main:app` | `https://api.example.com` |
| **Admin Service** | 관리자 UI 제공 (Streamlit) | `streamlit run admin.py` | `https://admin.example.com` |

---

## 3. Docker 빌드 전략 (Build Strategy)

### 3.1. 멀티 스테이지 빌드 (Multi-stage Build)
하나의 `Dockerfile` 내에서 `ARG`와 `Target`을 사용하여 환경별 이미지를 생성합니다.

- **Base**: 공통 OS 및 Python 패키지 설치
- **Development (Dev)**: 소스 코드 마운트, 핫 리로딩(Hot-reloading), 디버깅 툴 포함
- **Production (Prod)**: 소스 코드 복사(Copy), 최적화, 불변성 보장

### 3.2. Dockerfile 예시 규격
```dockerfile
# 1. Base Stage
FROM python:3.10-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Development Stage (Target: dev)
FROM base as dev
# 소스코드를 COPY하지 않고 볼륨 마운트 사용 (docker-compose 등)
ENV PYTHONPATH=/app/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

# 3. Production Stage (Target: prod)
FROM base as prod
# 소스코드를 이미지 내에 확정적으로 포함
COPY . .
ENV PYTHONPATH=/app/src
# 실행 명령어는 배포 시점에 덮어쓰거나 별도 스크립트 사용
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 4. 환경별 배포 가이드 (Deployment Guide)

### 4.1. 개발계 (Development)
빠른 반복 개발을 위해 로컬 볼륨 마운트 또는 개발용 컨테이너를 사용합니다.
- **빌드 명령**: `docker build --target dev -t myapp:dev .`
- **실행 특징**: 코드 수정 시 즉시 반영됨 (Hot-reload).

### 4.2. 운영계 (Production)
안정성과 불변성을 위해 소스 코드가 포함된 이미지를 빌드하여 배포합니다.
- **빌드 명령**: `docker build --target prod -t myapp:prod .`
- **배포 명령 (Cloud Run)**:
    ```bash
    # API 서비스 배포
    gcloud run deploy llm-api --image myapp:prod --command "uvicorn" --args "main:app" ...
    
    # Admin 서비스 배포
    gcloud run deploy llm-admin --image myapp:prod --command "streamlit" --args "run,streamlit/admin.py" ...
    ```

---

## 5. 비용 최적화 (Cost Optimization)

### 5.1. Scale to Zero
Cloud Run의 가장 큰 장점인 "요청이 없을 때 인스턴스 0개" 설정을 기본으로 합니다.
- **설정**: `min-instances: 0` (Default)
- **효과**: Admin 페이지와 같이 간헐적으로 사용되는 서비스의 비용을 **0원**에 가깝게 유지.



# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# UV 설치
RUN pip install --no-cache-dir uv

# 프로젝트 파일 복사
COPY pyproject.toml .
COPY .env.template .env

# 의존성 설치
RUN uv pip install --no-cache-dir -e .

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# UV 런타임에만 필요한 경우 설치
RUN pip install --no-cache-dir uv

# Stage 1에서 설치된 Python 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 프로젝트 코드 복사
COPY . .

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 헬스 체크 (API 선택)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# 기본 포트 노출
EXPOSE 8000 8501

# 기본 명령: API 서버 시작 (선택사항으로 변경 가능)
CMD ["uv", "run", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


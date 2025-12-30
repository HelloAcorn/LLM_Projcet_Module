# FastAPI 명세 (FastAPI Specification)

## 1. 개요 (Overview)
본 모듈(`api/main.py`)은 LLM 프로젝트 모듈의 RESTful 인터페이스를 정의합니다. **FastAPI**를 사용하여 고성능 비동기 엔드포인트를 제공하며, **ReDoc**을 통해 보안이 적용된 API 문서를 제공합니다.

## 2. 파일 경로 (File Path)
- `api/main.py`

## 3. 기본 설정 (Base Configuration)
- **Title**: LLM Project Module API
- **Version**: 1.0.0
- **Base URL**: `/api/v1` (버전별 엔드포인트)
- **Swagger URL**: `/docs` (개발자용)
- **ReDoc URL**: `/redoc` (배포용, Basic Auth 적용)

## 4. 미들웨어 (Middleware)
### 4.1. CORS
- **허용 출처 (Allowed Origins)**: `*` (개발 유연성을 위해 모든 출처 허용)
- **허용 메서드/헤더**: `*`

### 4.2. 요청 로깅 (`log_requests`)
모든 HTTP 요청을 가로채 레이턴시를 측정하고 메타데이터를 로깅합니다.
- **로그 파일**: `logs/api_requests.jsonl`
- **범위**: `/api/`를 포함하거나 `/health` 경로인 모든 요청.

### 4.3. 문서 보안 (`docs_auth`)
ReDoc 페이지(`/redoc`) 접근 시 Basic Authentication을 강제합니다.
- **의존성**: `src.core.config.settings` (`DOCS_USER`, `DOCS_PASSWORD`)
- **동작**:
    1. `/redoc` 요청을 가로챕니다.
    2. `secrets.compare_digest`를 사용하여 자격 증명을 검증합니다.
    3. 실패 시 401 Unauthorized를 반환합니다.

## 5. 의존성 (Dependencies)
- **External**: `fastapi`, `uvicorn`, `pydantic`, `python-multipart`
- **Internal**: `src.llm.llm_factory`, `src.core.config`

## 6. 실행 (Execution)
```bash
python api/main.py
# 또는
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

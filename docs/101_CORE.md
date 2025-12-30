# 핵심 모듈 명세 (Core Specification)

## 1. 개요 (Overview)
본 모듈(`src.core`)은 시스템의 기반 설정, 특히 API 키와 전역 상수를 관리합니다. `pydantic-settings`를 사용하여 전용 `.api_key` 파일에서 민감한 정보를 로드합니다.

## 2. 파일 경로 (File Path)
- `src/core/config.py`
- `src/core/.api_key` (설정 파일)

## 3. 의존성 (Dependencies)
- **External**: `pydantic-settings`, `pathlib`
- **Internal**: 없음

## 4. 클래스 시그니처 (Class Signature)

```python
class Settings(BaseSettings):
    """설정 구성 - API Keys 및 보안 설정 관리"""

    API_V1_STR: str = "/api"
    
    # LLM API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Documentation Security (ReDoc)
    DOCS_USER: str = "bigglz"
    DOCS_PASSWORD: str = "bigglz123!@#"

    class Config:
        case_sensitive = False
        env_file = Path(__file__).parent / ".api_key"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

settings = Settings()
```

## 5. 동작 로직 (Behavior Logic)

1.  **파일 경로 해석**: 본 모듈과 동일한 디렉토리(`src/core/`) 내에서 `.api_key` 파일을 찾습니다.
2.  **로드**: `utf-8` 인코딩을 사용하여 파일을 읽습니다.
3.  **파싱**: 키-값 쌍(예: `OPENAI_API_KEY=sk-...`)을 파싱하여 클래스 필드에 할당합니다.
4.  **인스턴스화**: 로드된 값으로 초기화된 싱글톤 인스턴스 `settings`를 생성합니다.

## 6. 사용 예시 (Usage Example)

```python
from src.core.config import settings

print(f"API 버전: {settings.API_V1_STR}")
print(f"문서 접근 사용자: {settings.DOCS_USER}")
```

## 7. 에러 처리 (Error Handling)

| 예외 (Exception) | 발생 조건 (Condition) |
|---|---|
| `ValidationError` | `.api_key` 파일의 값이 예상된 타입과 일치하지 않을 때. |
| `ConfigError` | `pydantic-settings`가 파일을 읽을 수 없을 때. |

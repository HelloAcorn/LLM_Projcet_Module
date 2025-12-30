# 핵심 모듈 명세 (Core Specification)

## 1. 개요 (Overview)
이 모듈(`src.core`)은 시스템의 기반 설정을 관리합니다. 환경 변수, API 키를 처리하고, 지원하는 LLM 모델의 가격 정책을 정의합니다.

## 2. 환경 설정 (`src/core/config.py`)

### 2.1. 시그니처 (Signature)
```python
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    GOOGLE_API_KEY: str
    
    # 프로젝트 설정
    PROJECT_NAME: str = "LLM Project Module"
    VERSION: str = "0.1.0"
```

### 2.2. 동작 로직 (Behavior Logic)
1.  **로드 (Loading)**: 시스템 환경 변수 또는 `.env` 파일에서 값을 읽어옵니다.
2.  **검증 (Validation)**: 필수 키(예: `OPENAI_API_KEY`)가 존재하는지 확인합니다.
3.  **접근 (Access)**: 싱글톤 인스턴스 `settings`를 통해 접근합니다.

---

## 3. 지원 모델 및 가격 (Supported Models & Pricing)

### 3.1. 개요
지원하는 LLM 모델 목록과 추정 비용을 정의합니다. 이 데이터는 `CostCallbackHandler`가 사용료를 계산하는 데 사용됩니다.

### 3.2. 가격표 (Pricing Table)
**단위: 1M 토큰당 USD ($)**

| 공급자 | 모델 ID | 입력 비용 ($) | 출력 비용 ($) | 비고 |
|---|---|---|---|---|
| **OpenAI** | `gpt-4o` | 5.00 | 15.00 | 고지능 |
| | `gpt-4o-mini` | 0.15 | 0.60 | 비용 효율 |
| **Anthropic** | `claude-3-5-sonnet-20240620` | 3.00 | 15.00 | 밸런스 |
| | `claude-3-haiku-20240307` | 0.25 | 1.25 | 고속 |
| **Gemini** | `gemini-1.5-pro` | 3.50 | 10.50 | 긴 컨텍스트 |
| | `gemini-1.5-flash` | 0.35 | 1.05 | 저지연 |

### 3.3. 설정 데이터 (`src/core/models.py`)
```python
SUPPORTED_MODELS = {
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},
    # ...
}
```

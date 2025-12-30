# LLM 팩토리 명세 (LLM Factory Specification)

## 1. 개요 (Overview)
본 모듈은 다양한 제공자(OpenAI, Anthropic, Gemini)의 LLM 인스턴스를 생성하는 **팩토리 패턴**을 구현합니다. 제공자별 고유 설정(예: GPT-5 `reasoning_effort`, Gemini 안전 설정)을 관리하며, 기본적으로 **구조화된 출력(JSON)**과 **비용 추적**을 강제합니다.

## 2. 파일 경로 (File Path)
- `src/llm/llm_factory.py`

## 3. 의존성 (Dependencies)
- **External**: `langchain`, `langchain-openai`, `langchain-anthropic`, `langchain-google-genai`, `pydantic`
- **Internal**: `app.core.settings`, `app.utils.decorators.measure_cost`

## 4. 클래스 시그니처 (Class Signature)

### 4.1. `create` (Factory Method)
```python
@staticmethod
def create(
    provider: Literal["openai", "anthropic", "gemini"],
    model: Optional[str] = None,
    temperature: float = 1.0,
    streaming: bool = False,
    json_schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
    **kwargs
) -> Runnable:
    ...
```

### 4.2. 헬퍼 메서드 (Helper Methods)
- `create_openai(...)`: OpenAI 전용 로직 처리 (예: GPT-5 온도 고정).
- `create_anthropic(...)`: Anthropic 전용 로직 처리.
- `create_gemini(...)`: Gemini 전용 로직 처리 (안전 설정, `top_k`/`top_p`).

## 5. 동작 로직 (Behavior Logic)

1.  **기본 모델 선택**: `model` 인자가 없으면 제공자별 기본 모델(예: `gpt-5-mini`)을 선택합니다.
2.  **제공자 분기 (Routing)**:
    -   **OpenAI**: GPT-5 모델의 경우 `reasoning_effort`를 지원(기본값 "medium")하며 `temperature`를 1.0으로 고정합니다.
    -   **Anthropic**: 표준 설정을 따릅니다.
    -   **Gemini**: 테스트 유연성을 위해 모든 `safety_settings`를 `BLOCK_NONE`으로 설정합니다.
3.  **비용 추적 주입**: `@measure_cost` 데코레이터를 통해 `callbacks`가 제공되지 않은 경우 `CostCallbackHandler`를 자동 주입합니다.
4.  **구조화된 출력 강제**:
    -   Base LLM을 `.with_structured_output(schema, include_raw=True)`로 래핑합니다.
    -   `json_schema`가 없으면 `DefaultJSONResponse`(`{"response": "..."}`)를 사용하여 JSON 일관성을 보장합니다.
5.  **신뢰성 (Reliability)**: 일시적 오류(예: Gemini 빈 응답)에 대응하기 위해 `.with_retry(stop_after_attempt=2)`를 추가합니다.

## 6. 사용 예시 (Usage Example)

```python
from src.llm.llm_factory import LLMFactory
from pydantic import BaseModel

# 1. 기본 사용 (기본 JSON 스키마)
llm = LLMFactory.create(provider="openai", model="gpt-4o")
response = llm.invoke("Hello")
print(response["parsed"].response)

# 2. 커스텀 스키마 사용
class UserInfo(BaseModel):
    name: str
    age: int

llm_custom = LLMFactory.create(
    provider="gemini",
    json_schema=UserInfo
)
response = llm_custom.invoke("내 이름은 김철수이고 30살이야.")
print(response["parsed"].name)  # 김철수
```

## 7. 에러 처리 (Error Handling)

| 예외 (Exception) | 발생 조건 (Condition) |
|---|---|
| `ValueError` | 지원하지 않는 `provider`가 지정되었을 때. |
| `ValueError` | 필수 API Key(예: `OPENAI_API_KEY`)가 설정에 없을 때. |

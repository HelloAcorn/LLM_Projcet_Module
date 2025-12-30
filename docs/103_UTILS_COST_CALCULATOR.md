# 비용 계산 및 추적 명세 (Cost Calculation & Tracking Specification)

## 1. 개요 (Overview)
본 모듈(`src.utils.callbacks`)은 **가격 정책(Pricing Policy)**을 정의하고, **CostCallbackHandler**를 구현하여 모든 LLM 호출 시 토큰 사용량과 예상 비용을 추적합니다. LangChain 생명주기의 미들웨어 역할을 수행합니다.

## 2. 파일 경로 (File Path)
- `src/utils/callbacks.py`

## 3. 의존성 (Dependencies)
- **External**: `langchain.callbacks.base.BaseCallbackHandler`, `langchain.schema.LLMResult`
- **Internal**: `src.core.config` (해당 시)

## 4. 가격 정책 (Pricing Policy)
**단위: 1M 토큰당 USD ($)**

```python
PRICING = {
    # OpenAI (GPT-5.2 Series)
    "gpt-5.2-chat-latest": {"input": 1.75, "output": 14.00}, # Instant
    "gpt-5.2": {"input": 1.75, "output": 14.00},             # Thinking
    "gpt-5-mini": {"input": 0.50, "output": 2.00},           # Legacy Mock
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},          # Legacy
    
    # Anthropic
    "claude-opus-4-5": {"input": 15.00, "output": 75.00},     # Mock Price
    "claude-sonnet-4-5": {"input": 4.00, "output": 16.00},    # Mock Price
    "claude-haiku-4-5": {"input": 0.25, "output": 1.25},      # Mock Price

    # Gemini
    "gemini-3-pro-preview": {"input": 4.00, "output": 12.00},   # Mock Price
    "gemini-3-flash-preview": {"input": 0.40, "output": 1.20}, # Mock Price
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40}   # Mock Price
}
```

## 5. 클래스 시그니처 (Class Signature)

```python
class CostCallbackHandler(BaseCallbackHandler):
    def __init__(self, log_path: str = "logs/cost.jsonl"): ...
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None: ...
    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float: ...
```

## 6. 동작 로직 (Behavior Logic)

### 6.1. 초기화 (Initialization)
- 로그 저장 디렉토리가 존재하지 않을 경우 생성합니다 (`os.makedirs`).

### 6.2. 토큰 추출 전략 (`on_llm_end`)
다음 순서로 `LLMResult`를 순회하며 토큰 사용량(Prompt/Completion/Total)을 찾습니다:
1.  **`response.llm_output`**: 일부 제공자의 기본 데이터 소스.
2.  **`response.generations`**:
    -   `generation_info['usage_metadata']`: 표준 LangChain 위치.
    -   `message.response_metadata['token_usage']`: OpenAI 스타일.
    -   `message.usage_metadata`: 메시지 객체 직접 속성.

### 6.3. 비용 계산 (`_calculate_cost`)
1.  **모델 매칭**: `PRICING` 딕셔너리에서 정확한 모델명을 조회합니다.
2.  **대체 (Fallback)**: 정확한 일치가 실패하면, `PRICING` 키가 모델명의 부분 문자열(Substring)인지 확인합니다 (예: `gpt-4o-2024`는 `gpt-4o` 가격 적용).
3.  **계산식**:
    $$ \text{Cost} = \left( \frac{\text{Input Tokens}}{1,000,000} \times \text{Input Price} \right) + \left( \frac{\text{Output Tokens}}{1,000,000} \times \text{Output Price} \right) $$

### 6.4. 로깅 (Logging)
- `log_path`에 JSON 객체를 추가(Append) 모드로 기록합니다.
- 포함 필드: `timestamp`, `model`, `tokens`, `cost`, `trace_id`.

## 7. 사용 예시 (Usage Example)

```python
from src.utils.callbacks import CostCallbackHandler
from langchain_openai import ChatOpenAI

# 핸들러 초기화
handler = CostCallbackHandler(log_path="logs/test_cost.jsonl")

# 핸들러와 함께 LLM 실행
llm = ChatOpenAI(model="gpt-4o-mini")
llm.invoke("Hello world", callbacks=[handler])
```

## 8. 에러 처리 (Error Handling)

| 예외 (Exception) | 발생 조건 (Condition) | 조치 (Action) |
|---|---|---|
| `Exception` (Generic) | 토큰 추출 또는 로깅 중 발생하는 모든 오류. | 내부적으로 `catch` 하여 stderr로 출력(`print`)하며, 메인 애플리케이션 흐름을 **중단시키지 않음(Non-blocking)**. |

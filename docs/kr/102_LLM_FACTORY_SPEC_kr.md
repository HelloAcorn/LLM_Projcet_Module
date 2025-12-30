# LLM Factory Specification

## 1. 개요 (Overview)
본 모듈은 **Factory Pattern**을 구현하여 표준화된 LLM 객체(OpenAI, Anthropic, Gemini)를 생성합니다. 공급자(Provider)별 구현을 추상화하고 기본적으로 **구조화된 출력(JSON)**을 강제하여 신뢰성을 보장합니다.

## 2. 의존성 (Dependencies)
- **Core**: `langchain-core`, `langchain-openai`, `langchain-anthropic`, `langchain-google-genai`
- **Internal**: `src.utils.callbacks.CostCallbackHandler`

## 3. 인터페이스 명세 (Interface Specification)

### 3.1. `create()` Method
제공자와 설정에 따라 Chat Model 인스턴스를 생성합니다.

#### Signature
```python
def create(
    provider: Literal["openai", "anthropic", "gemini"],
    model: Optional[str] = None,
    json_schema: Optional[Type[BaseModel]] = None,
    **kwargs
) -> BaseChatModel
```

#### Parameters
| 이름 | 타입 | 설명 | 필수 | 기본값 |
|---|---|---|---|---|
| `provider` | `str` | 대상 LLM 공급자 명 | 예 | - |
| `model` | `str` | 특정 모델 ID (예: `gpt-4o`) | 아니오 | 공급자 기본값 |
| `json_schema` | `Type[BaseModel]` | 구조화된 출력을 위한 Pydantic 모델 | 아니오 | `None` |
| `**kwargs` | `dict` | 추가 파라미터 (temperature, streaming 등) | 아니오 | - |

#### Return Value
- `BaseChatModel` (LangChain)을 상속받은 인스턴스를 반환합니다.
- `json_schema`가 제공된 경우, `.with_structured_output()`이 적용된 `Runnable` 시퀀스를 반환합니다.

## 4. 동작 로직 (Behavior Logic)

1.  **유효성 검사 (Validation)**: `provider`가 지원 목록(`openai`, `anthropic`, `gemini`)에 있는지 확인합니다. 유효하지 않으면 `ValueError`를 발생시킵니다.
2.  **인스턴스화 (Instantiation)**: 해당 LangChain 클래스(예: `ChatOpenAI`)를 사용하여 원시 LLM 객체를 생성합니다.
3.  **비용 추적 (Cost Tracking)**: `CostCallbackHandler`가 `callbacks` 리스트에 없다면 자동으로 주입합니다.
4.  **구조화된 출력 적용 (Structured Output Application)**:
    - `json_schema` 존재 시: 해당 스키마를 강제하도록 모델을 래핑합니다.
    - `json_schema` 미존재 시: 원시 모델을 반환하거나 설정에 따라 기본 일반 JSON 스키마를 적용합니다.

## 5. 사용 예시 (Usage Example)

```python
from src.llm.llm_factory import LLMFactory
from pydantic import BaseModel

# 스키마 정의
class UserIntent(BaseModel):
    intent: str
    confidence: float

# 모델 생성
llm = LLMFactory.create(
    provider="openai",
    model="gpt-4o",
    json_schema=UserIntent,
    temperature=0.0
)

# 실행
response = llm.invoke("서울행 비행기 예약해줘")
# response는 이제 UserIntent의 인스턴스임
print(response.intent)
```

## 6. 지원 모델 및 가격 (Supported Models & Pricing)
상세한 가격 및 모델 ID는 [103_SUPPORTED_MODELS_kr.md](103_SUPPORTED_MODELS_kr.md)를 참조하십시오.

## 7. 에러 처리 (Error Handling)

| 예외 (Exception) | 발생 조건 (Condition) |
|---|---|
| `ValueError` | 지원하지 않는 `provider` 이름이 제공되었을 때. |
| `ImportError` | 필수 공급자 패키지(예: `langchain_openai`)가 설치되지 않았을 때. |

# LLM Factory Specification (LLM 팩토리 명세)

## 1. 개요 (Overview)
다양한 LLM 제공자(OpenAI, Anthropic, Gemini)를 단일 팩토리 패턴 뒤로 추상화합니다. 신뢰성을 보장하기 위해 기본적으로 **Structured Output(JSON)**을 강제합니다.

**지원 모델 (Supported Models)**:
실제 지원되는 최신 모델 목록과 상세 스펙은 별도의 [SUPPORTED_MODELS.md](SUPPORTED_MODELS.md) 문서를 참조하십시오.

## 2. 인터페이스 계약 (Interface Contract)

### 2.1. 팩토리 메서드 (Factory Method)
```python
LLMFactory.create(
    provider: Literal["openai", "anthropic", "gemini"],
    model: Optional[str] = None,
    json_schema: Optional[Type[BaseModel]] = None,
    **kwargs
) -> BaseChatModel
```

### 2.2. 제공자 구현 요구사항 (Provider Requirements)
새로운 제공자를 추가할 경우 **반드시** 다음을 준수해야 합니다:
1. `BaseChatModel`을 상속받아야 한다.
2. `with_structured_output` 메서드를 지원해야 한다.
3. 표준 `temperature` 및 `streaming` 파라미터를 수용해야 한다.

## 3. 구조화된 출력 정책 (Structured Output Policy)
- **기본(Default)**: 스키마가 제공되지 않으면 팩토리가 자동으로 `DefaultJSONResponse`(범용 JSON 래퍼)를 주입합니다.
- **엄격 모드(Strict Mode)**: `json_schema`가 제공되면, LLM은 해당 Pydantic 모델과 일치하는 유효한 JSON만 출력하도록 강제됩니다.

## 4. 비용 및 관측성 (Cost & Observability)
팩토리는 사용량과 비용을 추적하기 위해 자동으로 관측성 후크(Hook)를 주입합니다.

### 4.1. 비용 로깅 (`logs/cost.jsonl`)
모든 LLM 호출에 대해 토큰 사용량과 추정 비용이 기록됩니다.

```json
{
  "timestamp": "2024-01-01T12:00:00.000Z",
  "model": "gpt-4o",
  "prompt_tokens": 50,
  "completion_tokens": 120,
  "total_tokens": 170,
  "cost": 0.0045,
  "trace_id": "req-123"
}
```

## 5. 사용 예시
```python
# 타 프로젝트에서의 사용 예
from llm.llm_factory import LLMFactory

# JSON 출력 및 비용 추적이 설정된 모델 인스턴스 반환
llm = LLMFactory.create(
    provider="openai", 
    model="gpt-4o",
    temperature=0.5
)
```

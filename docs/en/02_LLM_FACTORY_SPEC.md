# LLM Factory Specification

## 1. Overview
Abstracts LLM provider implementations (OpenAI, Anthropic, Gemini) behind a unified Factory pattern. Enforces structured outputs (JSON) by default to ensure reliability.

**Supported Models**:
For the full list of supported models and specifications, refer to [SUPPORTED_MODELS.md](SUPPORTED_MODELS.md).

## 2. Interface Contract

### 2.1. Factory Method
```python
LLMFactory.create(
    provider: Literal["openai", "anthropic", "gemini"],
    model: Optional[str] = None,
    json_schema: Optional[Type[BaseModel]] = None,
    **kwargs
) -> BaseChatModel
```

### 2.2. Provider Requirements
Any new provider implementation **MUST**:
1. Inherit from `BaseChatModel`.
2. Support `with_structured_output` method.
3. Accept standard `temperature` and `streaming` parameters.

## 3. Structured Output Policy
- **Default**: If no schema is provided, the factory injects `DefaultJSONResponse` (a generic JSON wrapper).
- **Strict Mode**: When `json_schema` is provided, the LLM is forced to output valid JSON matching that Pydantic model.

## 4. Cost & Observability
The Factory automatically injects observability hooks to track usage and cost.

### 4.1. Cost Logging (`logs/cost.jsonl`)
Every LLM invocation is logged with token usage and estimated cost.

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

## 5. Usage Example
```python
# Other Project Usage
from llm.llm_factory import LLMFactory

# Returns a model instance configured for JSON output and cost tracking
llm = LLMFactory.create(
    provider="openai", 
    model="gpt-4o",
    temperature=0.5
)
```


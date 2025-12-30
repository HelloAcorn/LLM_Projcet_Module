# LLM Factory Specification

## 1. Overview
This module implements the **Factory Pattern** to instantiate standardized LLM objects (OpenAI, Anthropic, Gemini). It abstracts provider-specific implementations and enforces **Structured Output (JSON)** by default to ensure reliability.

## 2. Dependencies
- **Core**: `langchain-core`, `langchain-openai`, `langchain-anthropic`, `langchain-google-genai`
- **Internal**: `src.utils.callbacks.CostCallbackHandler`

## 3. Interface Specification

### 3.1. `create()` Method
Instantiates a chat model based on the provider and configuration.

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
| Name | Type | Description | Required | Default |
|---|---|---|---|---|
| `provider` | `str` | Target LLM Provider name | Yes | - |
| `model` | `str` | Specific model ID (e.g., `gpt-4o`) | No | Provider Default |
| `json_schema` | `Type[BaseModel]` | Pydantic model for structured output | No | `None` |
| `**kwargs` | `dict` | Additional parameters (temperature, streaming) | No | - |

#### Return Value
- Returns an instance inheriting from `BaseChatModel` (LangChain).
- If `json_schema` is provided, returns a `Runnable` sequence with `.with_structured_output()`.

## 4. Behavior Logic

1.  **Validation**: Checks if `provider` is in the supported list (`openai`, `anthropic`, `gemini`). Raises `ValueError` if invalid.
2.  **Instantiation**: Creates the raw LLM object using the corresponding LangChain class (e.g., `ChatOpenAI`).
3.  **Cost Tracking**: Automatically injects `CostCallbackHandler` into the `callbacks` list if not present.
4.  **Structured Output Application**:
    - If `json_schema` is present: Wraps the model to enforce the schema.
    - If `json_schema` is None: Returns the raw model (or wraps with a default generic JSON schema if configured).

## 5. Usage Example

```python
from src.llm.llm_factory import LLMFactory
from pydantic import BaseModel

# Define Schema
class UserIntent(BaseModel):
    intent: str
    confidence: float

# Create Model
llm = LLMFactory.create(
    provider="openai",
    model="gpt-4o",
    json_schema=UserIntent,
    temperature=0.0
)

# Invoke
response = llm.invoke("Book a flight to Seoul")
# response is now an instance of UserIntent
print(response.intent)
```

## 6. Supported Models & Pricing
Refer to [103_SUPPORTED_MODELS.md](103_SUPPORTED_MODELS.md) for detailed pricing and model IDs.

## 7. Error Handling

| Exception | Condition |
|---|---|
| `ValueError` | Unsupported `provider` name provided. |
| `ImportError` | Required provider package (e.g., `langchain_openai`) is missing. |

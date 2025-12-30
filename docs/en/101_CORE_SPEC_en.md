# Core Specification

## 1. Overview
This module (`src.core`) manages the foundational configurations of the system. It handles environment variables, API keys, and defines the pricing policies for supported LLM models.

## 2. Environment Configuration (`src/core/config.py`)

### 2.1. Signature
```python
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    GOOGLE_API_KEY: str
    
    # Project Settings
    PROJECT_NAME: str = "LLM Project Module"
    VERSION: str = "0.1.0"
```

### 2.2. Behavior Logic
1.  **Loading**: Reads from system environment variables or a `.env` file.
2.  **Validation**: Ensures required keys (e.g., `OPENAI_API_KEY`) are present.
3.  **Access**: Accessed via a singleton instance `settings`.

---

## 3. Supported Models & Pricing

### 3.1. Overview
Defines the list of supported LLM models and their estimated costs. This data is used by `CostCallbackHandler` to calculate usage fees.

### 3.2. Pricing Table
**Unit: USD per 1M tokens**

| Provider | Model ID | Input Cost ($) | Output Cost ($) | Note |
|---|---|---|---|---|
| **OpenAI** | `gpt-4o` | 5.00 | 15.00 | High Intelligence |
| | `gpt-4o-mini` | 0.15 | 0.60 | Cost Efficient |
| **Anthropic** | `claude-3-5-sonnet-20240620` | 3.00 | 15.00 | Balanced |
| | `claude-3-haiku-20240307` | 0.25 | 1.25 | Fast |
| **Gemini** | `gemini-1.5-pro` | 3.50 | 10.50 | Large Context |
| | `gemini-1.5-flash` | 0.35 | 1.05 | Low Latency |

### 3.3. Configuration Data (`src/core/models.py`)
```python
SUPPORTED_MODELS = {
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},
    # ...
}
```

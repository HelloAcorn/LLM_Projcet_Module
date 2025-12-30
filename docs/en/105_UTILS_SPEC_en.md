# Utils Module Specification

## 1. Overview
This document defines the core utility modules located in `src/utils/`. These modules provide essential cross-cutting concerns: **Logging**, **Cost Tracking**, **Decorators**, and **Prompt Management**.

---

## 2. Logger (`src/utils/logger.py`)

### 2.1. Overview
Manages application-wide logs with a consistent format using the **Singleton Pattern**.

### 2.2. Signature
```python
class LoggerManager:
    @staticmethod
    def get_instance() -> 'LoggerManager': ...
    def get_logger(self) -> logging.Logger: ...
```

### 2.3. Behavior Logic
1.  **Singleton Check**: On `get_instance()`, checks if `_instance` exists. If not, creates one with thread-safe locking.
2.  **Configuration**: Sets log level (INFO/DEBUG), format (KST Timestamp), and handlers (StreamHandler/FileHandler) upon initialization.
3.  **Global Hook**: Registers `sys.excepthook` to capture unhandled exceptions globally.

### 2.4. Usage Example
```python
from src.utils.logger import LoggerManager

logger = LoggerManager.get_instance().get_logger()
logger.info("System initialized")
```

---

## 3. Callbacks (`src/utils/callbacks.py`)

### 3.1. Overview
Hooks into LangChain lifecycle events (`on_llm_end`) to calculate and log token usage and costs.

### 3.2. Signature
```python
class CostCallbackHandler(BaseCallbackHandler):
    def __init__(self, log_path: str = "logs/cost.jsonl"): ...
    def on_llm_end(self, response: LLMResult, **kwargs) -> None: ...
```

### 3.3. Behavior Logic
1.  **Event Trigger**: Triggered automatically when an LLM call finishes.
2.  **Token Extraction**: Parses `LLMResult` to find `token_usage` (adapts to OpenAI/Anthropic specific formats).
3.  **Cost Calculation**: Looks up unit price in `SUPPORTED_MODELS` and calculates: `(input_tokens * input_price) + (output_tokens * output_price)`.
4.  **Logging**: Appends a JSON record to the specified `log_path`.

### 3.4. Usage Example
```python
handler = CostCallbackHandler()
llm.invoke("Hi", callbacks=[handler])
```

---

## 4. Decorators (`src/utils/decorators.py`)

### 4.1. Overview
Reduces boilerplate code by automatically injecting dependencies like `CostCallbackHandler`.

### 4.2. Signature
```python
def measure_cost(func: Callable) -> Callable: ...
```

### 4.3. Behavior Logic
1.  **Interception**: Wraps the target function.
2.  **Injection**: Inspects `kwargs` for `callbacks`. If missing or empty, injects a new `CostCallbackHandler`.
3.  **Execution**: Calls the original function with the modified arguments.

### 4.4. Usage Example
```python
@measure_cost
def run_chat(prompt, callbacks=None):
    return llm.invoke(prompt, callbacks=callbacks)
```

---

## 5. Prompt Manager (`src/utils/prompt_manager.py`)

### 5.1. Overview
Loads and manages YAML-based prompt templates from the file system.

### 5.2. Signature
```python
class PromptManager:
    def load_template(self, file_name: str, key: str = "template") -> str: ...
```

### 5.3. Behavior Logic
1.  **Path Resolution**: Resolves `file_name` relative to `src/prompts/templates/`.
2.  **File Reading**: Opens file with UTF-8 encoding. Raises `FileNotFoundError` if missing.
3.  **Parsing**: Parses YAML content. Raises `YAMLError` on syntax errors.
4.  **Key Extraction**: Returns the value of the specified `key`. Raises `KeyError` if missing.

### 5.4. Usage Example
```python
manager = PromptManager()
system_prompt = manager.load_template("nfc_character.yaml", key="system_prompt")
```

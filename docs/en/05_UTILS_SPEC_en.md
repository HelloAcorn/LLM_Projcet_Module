# Utils Module Specification

## 1. Overview
This document defines the functions, interfaces, and implementation requirements of the common utility modules located in the `src/utils/` directory. These modules provide core functionalities such as logging, cost tracking, and prompt management that are reused throughout the system.

## 2. Logger (`src/utils/logger.py`)

### 2.1. Purpose
- Manages application-wide logs with a consistent format.
- Maintains a single instance via the Singleton pattern.

### 2.2. Key Features
- **Singleton Pattern**: Ensures a unique logger instance via `LoggerManager`.
- **Console Formatting**: Applies level-based coloring and timestamps based on KST (Korea Standard Time).
- **Global Exception Hook**: Automatically catches and logs uncaught exceptions.

### 2.3. Interface
```python
logger = LoggerManager.get_instance().get_logger()
logger.info("Message")
logger.error("Error Message")
```

## 3. Callbacks (`src/utils/callbacks.py`)

### 3.1. Purpose
- Hooks into the lifecycle events of LangChain-based LLM calls to track token usage and costs.

### 3.2. Key Features
- **Cost Tracking**: Extracts token usage upon `on_llm_end` event.
- **Universal Token Extraction**: Automatically parses response formats (llm_output, generation_info, message metadata) from various providers like OpenAI, Anthropic, and Gemini.
- **Pricing Calculation**: Calculates costs based on the model-specific unit prices defined in `02_LLM_FACTORY_SPEC`.
- **Logging**: Records calculated cost information to `logs/cost.jsonl` in JSON format.

### 3.3. Interface
```python
handler = CostCallbackHandler(log_path="logs/cost.jsonl")
# Pass as callbacks argument when calling LangChain models
```

## 4. Decorators (`src/utils/decorators.py`)

### 4.1. Purpose
- Simplifies the logic of injecting `CostCallbackHandler` repeatedly when calling functions.

### 4.2. Key Features
- **`@measure_cost`**: Checks the `callbacks` argument of the target function and automatically injects `CostCallbackHandler` if it is missing.

### 4.3. Usage Example
```python
@measure_cost
def invoke_llm(prompt, callbacks=[]):
    return llm.invoke(prompt, callbacks=callbacks)
```

## 5. Prompt Manager (`src/utils/prompt_manager.py`)

### 5.1. Purpose
- Loads and manages YAML-based prompt templates.

### 5.2. Key Features
- **YAML Loading**: Reads YAML files from the specified path with UTF-8 encoding.
- **Key Validation**: Validates the existence of a specific key (default: `template`).
- **Error Handling**: Raises explicit exceptions for file absence (`FileNotFoundError`) and missing keys (`KeyError`).

### 5.3. Interface
```python
# Load a single template
template_str = load_prompt("path/to/prompt.yaml", key="template")

# Load entire YAML
config = load_yaml("path/to/config.yaml")
```


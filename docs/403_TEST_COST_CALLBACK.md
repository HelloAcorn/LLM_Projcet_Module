# Cost Callback Test Specification

## 1. Overview
Tests the `src.utils.callbacks.CostCallbackHandler` to ensure precise token extraction and cost calculation across different providers.

## 2. Target Component
- **Component**: `src.utils.callbacks.CostCallbackHandler`
- **Spec Document**: `docs/103_UTILS_COST_CALCULATOR.md`

## 3. Test Cases (Unit)

### 3.1. Token Extraction (OpenAI Style)
- **Scenario**: Extract tokens from `response.llm_output`.
- **Input**: Mock `LLMResult` with `token_usage={"prompt_tokens": 100, "completion_tokens": 50}`.
- **Expected Output**: Prompt: 100, Completion: 50.

### 3.2. Token Extraction (Anthropic/Gemini Style)
- **Scenario**: Extract tokens from `usage_metadata` in message.
- **Input**: Mock `LLMResult` with `usage_metadata={"input_tokens": 100, "output_tokens": 50}`.
- **Expected Output**: Prompt: 100, Completion: 50.

### 3.3. Cost Calculation Logic
- **Scenario**: Verify math for a known model price.
- **Input**: Model: `gpt-4o-mini` (Input: $0.15, Output: $0.60), Tokens: 1M Input, 1M Output.
- **Expected Output**: Total Cost: $0.75 ($0.15 + $0.60).

### 3.4. Fallback Model Matching
- **Scenario**: Verify partial string matching for versioned models.
- **Input**: Model: `gpt-4o-2024-08-06`.
- **Expected Output**: Should match `gpt-4o` pricing.

### 3.5. Log File Writing
- **Scenario**: Ensure log entry is written to file.
- **Input**: Trigger `on_llm_end`.
- **Expected Output**: A new line JSON object in `logs/cost.jsonl` with correct fields.

## 4. Test Implementation Plan
- **File**: `tests/unit/test_cost_callback.py`
- **Tools**: `pytest`, `tempfile` (for log file testing).


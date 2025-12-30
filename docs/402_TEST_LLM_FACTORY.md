# LLM Factory Test Specification

## 1. Overview
Tests the `src.llm.llm_factory` to verify correct instantiation of LLM providers and enforcement of parameters (Temperature, Structured Output).

## 2. Target Component
- **Component**: `src.llm.llm_factory.LLMFactory`
- **Spec Document**: `docs/102_LLM_FACTORY.md`

## 3. Test Cases (Unit)

### 3.1. Factory Instantiation (OpenAI)
- **Scenario**: Create an OpenAI model instance.
- **Input**: `provider="openai"`, `model="gpt-4o"`, `temperature=0.5`.
- **Expected Output**: Returns a `Runnable` or `ChatOpenAI` instance with `temperature=0.5`.

### 3.2. GPT-5 Specific Logic
- **Scenario**: Verify parameter enforcement for GPT-5.
- **Input**: `provider="openai"`, `model="gpt-5-mini"`, `temperature=0.5`.
- **Expected Output**: `temperature` must be forced to `1.0`. `reasoning_effort` should be passed correctly.

### 3.3. Gemini Safety Settings
- **Scenario**: Verify that safety filters are disabled for Gemini.
- **Input**: `provider="gemini"`.
- **Expected Output**: `safety_settings` should contain `BLOCK_NONE` for all categories.

### 3.4. Invalid Provider Handling
- **Scenario**: Request an unsupported provider.
- **Input**: `provider="unknown_provider"`.
- **Expected Output**: Raise `ValueError`.

### 3.5. Cost Callback Injection
- **Scenario**: Check if `CostCallbackHandler` is automatically injected.
- **Input**: Call `create()` without `callbacks`.
- **Expected Output**: The returned model's `callbacks` list should contain an instance of `CostCallbackHandler`.

## 4. Test Implementation Plan
- **File**: `tests/unit/test_llm_factory.py`
- **Tools**: `pytest`, `pytest-mock` (to prevent actual API calls).


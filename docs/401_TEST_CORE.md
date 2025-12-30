# Core Module Test Specification

## 1. Overview
Tests the `src.core` module to ensure that environment variables and configurations are loaded correctly using `pydantic-settings`.

## 2. Target Component
- **Component**: `src.core.config.Settings`
- **Spec Document**: `docs/101_CORE.md`

## 3. Test Cases (Unit)

### 3.1. API Key Loading (Success)
- **Scenario**: Validate that API keys are correctly loaded from the `.api_key` file.
- **Input**: Mocked `.api_key` file content (`OPENAI_API_KEY=test-key`).
- **Expected Output**: `settings.OPENAI_API_KEY` should match "test-key".

### 3.2. Default Values
- **Scenario**: Validate that default values (e.g., `API_V1_STR`) are set correctly when not specified in the file.
- **Input**: Empty environment.
- **Expected Output**: `settings.API_V1_STR` should be "/api".

### 3.3. Singleton Behavior
- **Scenario**: Ensure `settings` is a singleton instance.
- **Input**: Import `settings` from `src.core.config` in two different places.
- **Expected Output**: Both instances should have the same memory address (Python module singleton).

## 4. Test Implementation Plan
- **File**: `tests/unit/test_core_config.py`
- **Tools**: `pytest`, `unittest.mock.patch` (for environment variables).


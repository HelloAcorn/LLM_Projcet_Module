# Prompt Manager Test Specification

## 1. Overview
Tests the `src.utils.prompt_manager.PromptManager` (functions `load_prompt`, `load_yaml`) for file I/O and error handling.

## 2. Target Component
- **Component**: `src.utils.prompt_manager`
- **Spec Document**: `docs/106_PROMPT_MANAGER.md`

## 3. Test Cases (Unit)

### 3.1. Successful Load
- **Scenario**: Load a valid YAML file.
- **Input**: YAML file with `template: "Hello"` content.
- **Expected Output**: Return "Hello".

### 3.2. File Not Found
- **Scenario**: Load a non-existent file.
- **Input**: Path `invalid/path.yaml`.
- **Expected Output**: Raise `FileNotFoundError`.

### 3.3. Key Error
- **Scenario**: Load a valid YAML missing the target key.
- **Input**: YAML with `content: "Hello"` (missing `template` key).
- **Expected Output**: Raise `KeyError`.

### 3.4. Invalid YAML Syntax
- **Scenario**: Load a corrupted file.
- **Input**: File with broken indentation/syntax.
- **Expected Output**: Raise `YAMLError` (or generic `Exception` depending on implementation wrapper).

## 4. Test Implementation Plan
- **File**: `tests/unit/test_prompt_manager.py`
- **Tools**: `pytest`, `tempfile` (to create temporary YAML files).


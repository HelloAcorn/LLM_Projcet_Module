# Prompt Specification

## 1. Overview
This document defines the YAML-based prompt template management architecture and the specifications for the `PromptManager` module. This structure separates prompts from application logic to enhance maintainability and allow non-developers to easily modify prompts.

## 2. Architecture
Prompts are managed as `yaml` files rather than hardcoded in source code, and are loaded at runtime via the `PromptManager`.

### 2.1. Directory Structure
```text
src/prompts/
├── prompt_manager.py  # Template loader and utilities
└── templates/         # YAML template repository
    ├── default_system.yaml
    ├── nfc_character.yaml
    └── ...
```

## 3. YAML Template Schema
All prompt template files must adhere to the following schema.

| Field | Type | Required | Description |
|---|---|---|---|
| `template` | `str` | **Yes** | The actual prompt text (supports Jinja2 style variables) |
| `input_variables` | `List[str]` | No | List of variables used within the template |
| `description` | `str` | No | Purpose and description of the template |
| `version` | `str` | No | Template version (e.g., "1.0.0") |

### Example (`templates/example.yaml`)
```yaml
description: "Default Chatbot System Prompt"
version: "1.0"
input_variables: ["role"]
template: |
  You are a helpful AI assistant.
  The user's role is {role}.
  Always respond kindly.
```

## 4. Prompt Manager (`src/prompts/manager.py`)

### 4.1. Functional Specs
- **Load Template**: Parses YAML via filename and returns the `template` string.
- **List Templates**: Provides a list of all available YAML files in the `templates/` directory.
- **Validation**: Checks for file existence and missing required fields (`template`).

### 4.2. Interface
```python
class PromptManager:
    @staticmethod
    def get_template_names() -> List[str]:
        """Returns a list of available template filenames"""
        pass

    @staticmethod
    def load_template(file_name: str) -> Dict[str, Any]:
        """Loads and parses a YAML file"""
        pass
```


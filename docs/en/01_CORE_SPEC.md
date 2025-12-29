# Core Module Specification

## 1. Overview
Defines the foundational configuration contracts required by all other modules.

## 2. Configuration Contract
The consuming application **MUST** provide a settings object or environment variables matching the following schema.

### 2.1. Required Environment Variables
| Variable | Description | Required For |
|----------|-------------|--------------|
| `OPENAI_API_KEY` | OpenAI API Key | `openai` provider |
| `ANTHROPIC_API_KEY` | Anthropic API Key | `anthropic` provider |
| `GEMINI_API_KEY` | Google Gemini API Key | `gemini` provider |
| `VECTOR_STORE_PATH` | Path to persist vector DB | RAG Module |

# Admin Console Specification

## 1. Overview
The Admin Console serves as a unified hub for **Operational Observability** and **Prompt Experimentation (Playground)**. It provides real-time cost tracking and API performance monitoring for LLM-based services.

---

## 2. Dashboard
Visualizes economic and technical performance metrics of the system.

### 2.1. LLM Cost & Usage
- **Data Source**: `logs/cost.jsonl`
- **Key Metrics**:
    - **Total Cost**: Cumulative estimated cost of all LLM calls (USD).
    - **Total Tokens**: Total number of tokens consumed.
    - **LLM Calls**: Total number of successful LLM invocations.
- **Visualizations**:
    - Daily cost trend per model (Bar Chart).
    - Usage distribution per model (Pie Chart).

### 2.2. API Performance
- **Data Source**: `logs/api_requests.jsonl`
- **Endpoint Summary (Table)**:
    - **Requests**: Total number of requests per endpoint.
    - **Avg/P95 Latency**: Average and 95th percentile response times (ms).
    - **Success Rate**: Percentage of HTTP 200 responses (%).

---

## 3. Developer Tools (Playground)
Test prompts in a sandbox environment and validate model responses.

### 3.1. Settings & Parameters
- **Model Selection**: Synced with `src.utils.callbacks.SUPPORTED_MODELS`.
- **Auto Provider Detection**: Automatically assigns OpenAI, Anthropic, or Gemini based on the selected model name.
- **Temperature**: Adjust response creativity via a slider.

### 3.2. Template Manager
- **Location**: `src/prompts/templates/*.yaml`
- **Functionality**: Parses YAML templates and loads the `template` field directly into the system prompt area.
- **Format**: Recommended YAML schema including a `template` field.

### 3.3. Chat & Utilities
- **System Prompt Editor**: Edit personas and constraints in real-time.
- **Download Chat History**: Save the current conversation as a JSON file locally.
- **Real-time Logging**: Inspect raw responses (Parsed vs Raw) and detailed cost logs via the terminal/debug logs.

---

## 4. Data Contract

### 4.1. Cost Log Schema (`cost.jsonl`)
```json
{
  "timestamp": "ISO8601",
  "model": "gpt-5.2-chat-latest",
  "prompt_tokens": 120,
  "completion_tokens": 80,
  "total_tokens": 200,
  "cost": 0.00035,
  "trace_id": "uuid-string"
}
```

### 4.2. API Request Log Schema (`api_requests.jsonl`)
```json
{
  "timestamp": "ISO8601",
  "method": "POST",
  "path": "/api/v1/chat",
  "status_code": 200,
  "latency_ms": 450.5
}
```

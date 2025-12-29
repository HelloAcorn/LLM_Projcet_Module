# Supported Models

This document defines the detailed specifications of models officially supported by `LLMFactory` (including future 2025 models).

## 1. OpenAI (GPT-5 Series)
| Model ID | Alias | Feature | Description |
|----------|-------|---------|-------------|
| `gpt-5.2-thinking`| **Thinking** | Extended Thinking | Specialized for complex reasoning tasks with deep thought chains. |
| `gpt-5.2-high` | **High-Perf** | High Performance | Flagship model with maximum intelligence and accuracy. |
| `gpt-5-mini` | **Mini** | Balanced | Lightweight version maintaining GPT-5 capabilities. |
| `gpt-4o-mini` | **Legacy Mini**| Cost Effective | Ultra-low cost, high-efficiency model based on GPT-4o. |

## 2. Anthropic (Claude 4.5 Series)
| Model ID | Alias | Feature | Description |
|----------|-------|---------|-------------|
| `claude-4.5-opus` | **Opus** | Max Intelligence | Highest reasoning capability and creativity. |
| `claude-4.5-sonnet`| **Sonnet** | Balanced | Perfect balance of speed and intelligence. |
| `claude-4.5-haiku` | **Haiku** | Speed | Ultra-fast model for instant response tasks. |

## 3. Google Gemini (Gemini 3 Series)
| Model ID | Alias | Feature | Description |
|----------|-------|---------|-------------|
| `gemini-3.0-pro` | **Pro** | Multimodal Powerhouse | Optimized for massive context and multimodal processing. |
| `gemini-3.0-flash` | **Flash** | Low Latency | Low-latency lightweight version of Gemini 3. |
| `gemini-2.5-flash-lite`| **Lite** | Ultra Light | Ultra-light/low-cost model comparable to edge devices. |

---
**Note**:
- Use these Model IDs as the `model` parameter when calling `LLMFactory.create()`.

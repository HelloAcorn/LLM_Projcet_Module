# 지원 모델 목록 (Supported Models)

이 문서는 `LLMFactory`에서 공식적으로 지원하는 모델의 상세 스펙을 정의합니다. (2025년 기준 미래 시점 모델 포함)

## 1. OpenAI (GPT-5 Series)
| 모델 ID (Model ID) | 별칭 (Alias) | 특징 | 설명 |
|-------------------|-------------|------|------|
| `gpt-5.2-thinking`| **Thinking** | Extended Thinking | 복잡한 추론 작업에 특화된 심층 사고 모델. |
| `gpt-5.2-high` | **High-Perf** | High Performance | 가장 높은 지능과 정확도를 가진 플래그십 모델. |
| `gpt-5-mini` | **Mini** | Balanced | GPT-5의 성능을 유지하면서 경량화된 모델. |
| `gpt-4o-mini` | **Legacy Mini**| Cost Effective | GPT-4o 기반의 초저비용 고효율 모델. |

## 2. Anthropic (Claude 4.5 Series)
| 모델 ID (Model ID) | 별칭 (Alias) | 특징 | 설명 |
|-------------------|-------------|------|------|
| `claude-4.5-opus` | **Opus** | Max Intelligence | 가장 뛰어난 추론 능력과 창의성을 가진 모델. |
| `claude-4.5-sonnet`| **Sonnet** | Balanced | 속도와 지능의 균형이 완벽한 표준 모델. |
| `claude-4.5-haiku` | **Haiku** | Speed | 즉각적인 응답이 필요한 작업을 위한 초고속 모델. |

## 3. Google Gemini (Gemini 3 Series)
| 모델 ID (Model ID) | 별칭 (Alias) | 특징 | 설명 |
|-------------------|-------------|------|------|
| `gemini-3.0-pro` | **Pro** | Multimodal Powerhouse | 대규모 컨텍스트와 멀티모달 처리에 최적화된 모델. |
| `gemini-3.0-flash` | **Flash** | Low Latency | Gemini 3 기반의 저지연 경량 버전. |
| `gemini-2.5-flash-lite`| **Lite** | Ultra Light | 엣지 디바이스 수준의 초경량/초저비용 모델. |

---
**주의사항**:
- 위 모델 ID들은 `LLMFactory.create()` 호출 시 `model` 파라미터로 사용됩니다.

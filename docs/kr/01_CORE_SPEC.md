# Core Module Specification (핵심 모듈 명세)

## 1. 개요 (Overview)
모든 모듈에서 공통적으로 요구되는 기본 설정 계약(Configuration Contract)을 정의합니다.

## 2. 설정 계약 (Configuration Contract)
이 모듈을 사용하는 애플리케이션은 반드시 아래 스키마에 맞는 설정 객체나 환경 변수(Environment Variables)를 제공해야 합니다.

### 2.1. 필수 환경 변수
| 변수명 | 설명 | 필수 조건 |
|--------|------|-----------|
| `OPENAI_API_KEY` | OpenAI API 키 | `openai` 프로바이더 사용 시 |
| `ANTHROPIC_API_KEY` | Anthropic API 키 | `anthropic` 프로바이더 사용 시 |
| `GEMINI_API_KEY` | Google Gemini API 키 | `gemini` 프로바이더 사용 시 |
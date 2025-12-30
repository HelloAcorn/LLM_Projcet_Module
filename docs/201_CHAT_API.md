# 채팅 API 명세 (Chat API Specification)

## 1. 개요 (Overview)
본 모듈(`api/main.py`)은 `LLMFactory`를 활용하여 다양한 LLM과 대화를 수행하는 핵심 엔드포인트를 정의합니다. 동적인 모델 선택, 메시지 포맷 변환, 구조화된 응답 처리를 지원합니다.

## 2. 파일 경로 (File Path)
- `api/main.py`

## 3. 엔드포인트 시그니처 (Endpoint Signature)
- **Method**: `POST`
- **Path**: `/api/v1/chat`
- **Summary**: LLM 기반 채팅 인터페이스

## 4. 데이터 모델 (Data Models)

### 4.1. 요청 (`ChatRequest`)
| 필드 (Field) | 타입 (Type) | 설명 (Description) | 기본값 (Default) |
|---|---|---|---|
| `chat_list` | `List[Message]` | 대화 이력 객체 리스트 (`role`, `content`) | 필수 |
| `user_message` | `str` | 현재 사용자 입력 메시지 | 필수 |
| `uid` | `str` | 사용자 식별 ID (로깅/추적용) | `None` |
| `lang` | `str` | 응답 언어 코드 (ISO 639-1) | `"ko"` |
| `model` | `str` | 사용할 LLM 모델 식별자 | `"gemini-2.5-flash-lite"` |
| `temperature` | `float` | 생성 다양성 조절 파라미터 (0.0 ~ 2.0) | `0.7` |

### 4.2. 응답 (`ChatResponse`)
| 필드 (Field) | 타입 (Type) | 설명 (Description) |
|---|---|---|
| `responses` | `List[str]` | 생성된 응답 텍스트 리스트 |

## 5. 동작 로직 (Behavior Logic)
1.  **제공자 결정 (Provider Resolution)**: 요청된 `model` 문자열(예: `gpt-4o`, `claude-3-5`)을 분석하여 적절한 Provider(`openai`, `anthropic`, `gemini`)를 자동으로 선택합니다.
2.  **팩토리 생성 (Factory Creation)**: `LLMFactory.create()`를 호출하여 설정된 파라미터(`temperature` 등)를 가진 LLM 인스턴스를 생성합니다.
3.  **메시지 변환 (Message Conversion)**: `ChatRequest`의 `chat_list`를 LangChain 호환 객체(`SystemMessage`, `HumanMessage`)로 변환합니다.
4.  **실행 (Invocation)**: 변환된 메시지 리스트로 LLM을 호출하고, 결과를 파싱합니다.
    -   구조화된 출력(JSON)일 경우 `parsed.response` 필드를 추출합니다.
    -   일반 문자열일 경우 그대로 반환합니다.
5.  **반환 (Return)**: 최종 응답 문자열을 리스트에 담아 `ChatResponse` 객체로 반환합니다.

## 6. 사용 예시 (Usage Example)
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "chat_list": [{"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}],
           "user_message": "최신 AI 트렌드에 대해 알려줘",
           "model": "gpt-4o-mini",
           "temperature": 0.5
         }'
```

## 7. 에러 처리 (Error Handling)

| 예외 (Exception) | 상태 코드 (Status) | 설명 (Description) |
|---|---|---|
| `ValueError` | 422 Unprocessable Entity | 지원하지 않는 모델명이나 잘못된 입력 데이터 형식. |
| `Exception` | 500 Internal Server Error | LLM 제공자 API 오류 또는 내부 로직 실패. |

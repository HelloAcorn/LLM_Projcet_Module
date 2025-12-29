# HTTP API Specification (HTTP API 명세)

## 1. 개요 (Overview)
FastAPI를 사용하여 핵심 기능을 REST 엔드포인트로 노출합니다. 본 문서는 채팅 서비스의 표준 입력/반환 규격을 정의합니다.

## 2. 공통 데이터 모델 (Common Data Models)

### 2.1. Message (대화 내역)
대화의 각 턴을 나타내는 객체입니다.

| 필드명 | 타입 | 설명 | 필수 여부 |
|--------|------|------|-----------|
| `role` | str | `user` 또는 `assistant` | Yes |
| `content`| str | 메시지 내용 | Yes |

```json
{
  "role": "user",
  "content": "안녕하세요"
}
```

## 3. API 엔드포인트 (Endpoints)

### 3.1. 기본 채팅 API (Basic Chat API)
범용적인 LLM 채팅을 위한 표준 규격입니다.

- **URL**: `POST /api/v1/chat/basic`

#### 입력 규격 (Request)
| 필드명 | 타입 | 설명 |
|--------|------|------|
| `chat_list` | `List[Message]` | 이전 대화 내역 |
| `user_message` | `str` | 현재 유저 입력 |
| `uid` | `str` | (Optional) 유저 식별자 |
| `lang` | `str` | (Optional) 언어 코드 |

```json
{
  "chat_list": [
    {"role": "user", "content": "안녕"},
    {"role": "assistant", "content": "반갑습니다."}
  ],
  "user_message": "자기소개 해줘",
  "uid": "user_123"
}
```

#### 반환 규격 (Response)
| 필드명 | 타입 | 설명 |
|--------|------|------|
| `responses` | `List[str]` | 생성된 응답 목록 (보통 1개) |

```json
{
  "responses": [
    "저는 인공지능 어시스턴트입니다."
  ]
}
```

---

### 3.2. NFC 채팅 API (NFC Chat API)
캐릭터 페르소나와 감정 표현이 포함된 특화 채팅 규격입니다.

- **URL**: `POST /api/v1/chat/nfc`

#### 입력 규격 (Request)
| 필드명 | 타입 | 설명 |
|--------|------|------|
| `chat_list` | `List[Message]` | 이전 대화 내역 |
| `user_message` | `str` | 현재 유저 입력 |
| `lang` | `str` | 언어 코드 (예: `ko`, `en`) |
| `character_code`| `int` | 캐릭터 식별 코드 |
| `team_code` | `str` | (Optional) 팀 코드 |
| `uuid` | `str` | (Optional) 고유 식별자 |

#### 반환 규격 (Response)
기본 응답 외에 감정(motion) 정보가 포함될 수 있습니다.

| 필드명 | 타입 | 설명 |
|--------|------|------|
| `responses` | `List[str]` | 응답 문자열 목록 |
| `emotion` | `str` | (Optional) 감정 상태<br>`joyful`, `surprise`, `anger`, `sadness`, `encourage`, `excited`, `neutral` |
| `degree` | `int` | (Optional) 감정 강도 (1~3) |

```json
{
  "responses": [
    "정말 기쁜 소식이네요!"
  ],
  "emotion": "joyful",
  "degree": 3
}
```

# HTTP API Specification

## 1. Overview
Exposes core functionalities via REST endpoints using FastAPI. This document defines the standard input/output schemas for chat services.

## 2. Common Data Models

### 2.1. Message
Represents a single turn in the conversation.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `role` | str | `user` or `assistant` | Yes |
| `content`| str | Message content | Yes |

```json
{
  "role": "user",
  "content": "Hello"
}
```

## 3. Endpoints

### 3.1. Basic Chat API
Standard specification for general-purpose LLM chat.

- **URL**: `POST /api/v1/chat/basic`

#### Request Schema
| Field | Type | Description |
|-------|------|-------------|
| `chat_list` | `List[Message]` | Conversation history |
| `user_message` | `str` | Current user input |
| `uid` | `str` | (Optional) User ID |
| `lang` | `str` | (Optional) Language code |

```json
{
  "chat_list": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello there."}
  ],
  "user_message": "Who are you?",
  "uid": "user_123"
}
```

#### Response Schema
| Field | Type | Description |
|-------|------|-------------|
| `responses` | `List[str]` | List of generated responses |

```json
{
  "responses": [
    "I am an AI assistant."
  ]
}
```

---

### 3.2. NFC Chat API
Specialized chat specification including character persona and emotion.

- **URL**: `POST /api/v1/chat/nfc`

#### Request Schema
| Field | Type | Description |
|-------|------|-------------|
| `chat_list` | `List[Message]` | Conversation history |
| `user_message` | `str` | Current user input |
| `lang` | `str` | Language code (e.g., `ko`, `en`) |
| `character_code`| `int` | Character identifier |
| `team_code` | `str` | (Optional) Team code |
| `uuid` | `str` | (Optional) Unique identifier |

#### Response Schema
May include emotion/motion information alongside the text response.

| Field | Type | Description |
|-------|------|-------------|
| `responses` | `List[str]` | List of response strings |
| `emotion` | `str` | (Optional) Emotion state<br>`joyful`, `surprise`, `anger`, `sadness`, `encourage`, `excited`, `neutral` |
| `degree` | `int` | (Optional) Emotion intensity (1~3) |

```json
{
  "responses": [
    "That is great news!"
  ],
  "emotion": "joyful",
  "degree": 3
}
```

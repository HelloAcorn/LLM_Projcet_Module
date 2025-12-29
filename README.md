# LLM Project Module

팩토리 메서드 기반 LLM 프로젝트 골격. 최소화 원칙, Settings는 싱글톤, core는 고정하고 필요한 모듈만 확장.

---

## 디렉토리 구조
```
LLM_Project_Module/
├── pyproject.toml
├── .env.template
│
├── src/
│   ├── core/                   # [필수 - 변경 금지]
│   │   ├── settings.py         # Singleton: 전역 설정
│   ├── llm/     
│   │   └── llm_factory.py      # Factory: LLM 생성 (OpenAI/Anthropic/Gemini 통합)
│   │
│   └── utils/                  # [선택]
│       └── logger.py
│
│   # 아래는 필요시 추가
│   ├── embeddings/
│   ├── vectorstore/
│   ├── retrieval/
│   ├── agents/
│   └── data/
│
├── streamlit/                  # [선택] UI
├── api/                        # [선택] REST API
│
├── logs/
│   ├── app.log                 # 텍스트
│   ├── llm_calls.jsonl         # LLM 호출 기록
│   └── cost.jsonl              # 비용
│
├── Dockerfile
└── docker-compose.yml
```

---

## 핵심 아키텍처

**LLM Factory (통합 관리)**
- 파일: `src/llm/llm_factory.py`
- 책임: OpenAI/Anthropic/Gemini 통합 관리, 모델별 파라미터 처리, Structured Output 자동 적용
- 사용: `LLMFactory.create("openai", model="gpt-5-mini", json_schema=MySchema)`
- **변경 금지**: 이 파일은 프로젝트 골격의 핵심이므로 수정하지 않음

**Singleton (Settings)**
- 파일: `src/core/settings.py`
- 책임: API 키 로드 (OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY)
- 사용: `Settings()` 어디서든 동일 인스턴스

---


## 모듈 추가 규칙

**RAG 필요** → `vectorstore/`, `retrieval/` 폴더 생성  
**UI/API 필요** → `streamlit/` 또는 `api/` 활성화  
**단순 유틸** → 5개 미만 함수면 `utils/` 단일 파일, 5개 이상이면 폴더

---

## 문서화 규칙 (Documentation Rules)

**Spec First & Sync Policy**:
1.  모든 기능 변경 및 추가 작업은 `docs/`의 Spec 문서를 기준으로 수행해야 합니다.
2.  **코드를 수정한 후에는 반드시 관련 Spec 문서(`docs/en`, `docs/kr`)를 확인하고 동기화해야 합니다.**
3.  Spec 문서의 변경이 필요한 경우, **영문(en)과 국문(kr) 버전을 동시에 수정**해야 합니다.
4.  구현 코드와 Spec 문서가 일치하지 않는 상태(Documentation Drift)는 엄격히 금지됩니다.

---

## 금지 사항

**하지 말 것**:
- `llm/llm_factory.py` 수정 (고정된 골격)
- 5개 미만 함수/클래스로 폴더 생성
- Settings 없이 API 키 하드코딩
- LLM 직접 인스턴스화 (반드시 Factory 사용)

**반드시 할 것**:
- 모든 LLM 생성은 LLMFactory 사용
- API 키는 Settings로 중앙 관리
- JSON 응답 필요 시 Pydantic 스키마 정의

---

## 환경 변수

`.env`:
```
# API Keys
ANTHROPIC_API_KEY=YOUR_API_KEY
OPENAI_API_KEY=YOUR_API_KEY
GEMINI_API_KEY=YOUR_API_KEY
```

---

## 의존성
uv로 실행하고, 의존성에 필요한 모듈 추가

---

## 개발 순서

1. core 세팅 (settings, llm_factory는 이미 구현됨)
2. 필요한 모듈 구현 (목적에 맞게)
3. UI/API 추가 (선택)

---

## LLM Factory 사용 예시

**기본 사용**:
```python
llm = LLMFactory.create("openai")  # gpt-5-mini
response = llm.invoke("Hello")
```

**모델 지정**:
```python
llm = LLMFactory.create("gemini", model="gemini-2.5-pro")
```

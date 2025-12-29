# 관리자 콘솔 명세 (Admin Console Specification)

## 1. 개요 (Overview)
관리자 콘솔은 LLM 서비스의 **운영 관측성(Observability)**과 **프롬프트 실험(Playground)**을 위한 통합 허브입니다. 실시간 비용 추적과 API 성능 모니터링 기능을 제공합니다.

---

## 2. 대시보드 (Dashboard)
시스템의 경제적 지표와 기술적 성능 지표를 시각화합니다.

### 2.1. LLM 비용 및 사용량 (LLM Cost & Usage)
- **데이터 소스**: `logs/cost.jsonl`
- **주요 지표**:
    - **Total Cost**: 모든 모델 호출에 대한 누적 추정 비용 (USD).
    - **Total Tokens**: 소비된 총 토큰 수.
    - **LLM Calls**: 총 LLM 호출 횟수.
- **시각화**:
    - 모델별 일일 비용 추이 (Bar Chart).
    - 모델별 사용 비중 (Pie Chart).

### 2.2. API 성능 (API Performance)
- **데이터 소스**: `logs/api_requests.jsonl`
- **엔드포인트별 요약 (Table)**:
    - **Requests**: 엔드포인트별 총 요청 수.
    - **Avg/P95 Latency**: 평균 및 상위 95% 응답 속도 (ms).
    - **Success Rate**: HTTP 200 응답 비율 (%).

---

## 3. 개발자 도구 (Playground)
샌드박스 환경에서 프롬프트를 테스트하고 모델 응답을 검증합니다.

### 3.1. 설정 및 파라미터 (Settings)
- **모델 선택**: `src.utils.callbacks.SUPPORTED_MODELS`에 정의된 최신 모델 목록과 연동.
- **프로바이더 자동 감지**: 선택된 모델명에 따라 OpenAI, Anthropic, Gemini 자동 할당.
- **온도(Temperature)**: 슬라이더를 통해 응답의 창의성 조절.

### 3.2. 템플릿 관리자 (Template Manager)
- **위치**: `src/prompts/templates/*.yaml`
- **기능**: YAML 형식의 템플릿을 파싱하여 시스템 프롬프트 영역으로 즉시 로드.
- **포맷**: `template` 필드를 포함한 YAML 규격 권장.

### 3.3. 채팅 및 유틸리티
- **시스템 프롬프트 편집**: 페르소나 및 제약 사항 실시간 수정.
- **채팅 이력 다운로드**: 현재 대화 내용을 JSON 형식으로 로컬 저장.
- **실시간 로깅**: 터미널을 통해 Raw Response(Parsed vs Raw) 및 상세 비용 로그 확인 가능.

---

## 4. 데이터 계약 (Data Contract)

### 4.1. 비용 로그 스키마 (`cost.jsonl`)
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

### 4.2. API 요청 로그 스키마 (`api_requests.jsonl`)
```json
{
  "timestamp": "ISO8601",
  "method": "POST",
  "path": "/api/v1/chat",
  "status_code": 200,
  "latency_ms": 450.5
}
```

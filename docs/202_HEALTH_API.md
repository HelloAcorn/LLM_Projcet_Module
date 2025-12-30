# 헬스 체크 API 명세 (Health Check API Specification)

## 1. 개요 (Overview)
본 모듈(`api/main.py`)은 API 서버의 가동 상태를 확인하기 위한 경량 엔드포인트를 제공합니다. 로드 밸런서(L4/L7), 오케스트레이터(K8s), 또는 모니터링 도구에서 서버의 생존 여부(Liveness)를 판단하는 데 사용됩니다.

## 2. 파일 경로 (File Path)
- `api/main.py`

## 3. 엔드포인트 시그니처 (Endpoint Signature)
- **Method**: `GET`
- **Path**: `/health`
- **Summary**: 서버 상태 확인 (Health Check)

## 4. 응답 스키마 (Response Schema)
서버의 현재 상태 정보를 담은 JSON 객체를 반환합니다.

```json
{
  "status": "healthy",
  "service": "LLM Project Module API"
}
```

## 5. 동작 로직 (Behavior Logic)
1.  **요청 수신 (Request)**: HTTP GET 요청을 받습니다.
2.  **즉시 응답 (Response)**: 별도의 비즈니스 로직이나 DB 연결 확인 없이 정적인 상태 메시지를 즉시 반환합니다. 이는 오버헤드를 최소화하기 위함입니다.
3.  **로깅 (Logging)**: `log_requests` 미들웨어를 통해 해당 요청의 처리 시간과 상태 코드가 `logs/api_requests.jsonl`에 기록됩니다.

## 6. 사용 예시 (Usage Example)
```bash
curl "http://localhost:8000/health"
# 출력: {"status":"healthy", "service":"LLM Project Module API"}
```

## 7. 에러 처리 (Error Handling)
본 엔드포인트는 내부 로직이 없으므로 예외 발생 가능성이 극히 낮으나, 서버 자체가 다운된 경우 응답이 없습니다.

| 상태 코드 (Status) | 설명 (Description) |
|---|---|
| 200 OK | 서버가 정상적으로 작동 중임. |
| Connection Refused | 서버 프로세스가 실행 중이지 않거나 포트가 닫혀 있음. |

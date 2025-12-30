# 로거 유틸리티 명세 (Logger Utility Specification)

## 1. 개요 (Overview)
본 모듈(`src.utils.logger`)은 애플리케이션 전역에서 일관된 포맷과 정책을 가진 로그 시스템을 제공하며, **싱글톤 패턴(Singleton Pattern)**을 통해 단일 인스턴스를 보장합니다.

## 2. 파일 경로 (File Path)
- `src/utils/logger.py`

## 3. 의존성 (Dependencies)
- **External**: `logging` (Python Standard Library), `sys`
- **Internal**: `src.core.config` (로그 레벨 설정용)

## 4. 클래스 시그니처 (Class Signature)
```python
class LoggerManager:
    _instance: Optional['LoggerManager'] = None

    @staticmethod
    def get_instance() -> 'LoggerManager':
        """싱글톤 인스턴스를 반환합니다."""
        ...

    def get_logger(self) -> logging.Logger:
        """설정된 로거 객체를 반환합니다."""
        ...
```

## 5. 동작 로직 (Behavior Logic)

1.  **초기화 (Initialization)**: `get_instance()` 호출 시, `_instance`가 없으면 클래스를 인스턴스화합니다. 이때 스레드 락(Lock)을 사용하여 동시성 이슈를 방지합니다.
2.  **설정 (Configuration)**:
    -   로그 레벨: 환경 변수(DEBUG/INFO)에 따릅니다.
    -   포맷: `[Timestamp] [Level] [Message]` 형태 (KST 시간 기준).
    -   핸들러: 콘솔(StreamHandler) 및 파일(FileHandler) 출력을 동시에 지원합니다.
3.  **전역 예외 처리 (Global Exception Hook)**: `sys.excepthook`을 재정의하여, 처리되지 않은(Uncaught) 예외가 발생했을 때 프로그램이 조용히 종료되지 않고 로그에 `CRITICAL` 레벨로 기록되도록 합니다.

## 6. 사용 예시 (Usage Example)

```python
from src.utils.logger import LoggerManager

# 로거 인스턴스 획득
logger = LoggerManager.get_instance().get_logger()

# 로그 기록
logger.info("Application started successfully.")
try:
    1 / 0
except ZeroDivisionError:
    logger.error("Division by zero occurred", exc_info=True)
```

## 7. 에러 처리 (Error Handling)

| 예외 (Exception) | 발생 조건 (Condition) |
|---|---|
| `ImportError` | `logging` 모듈 로드 실패 시 (매우 드묾). |
| `PermissionError` | 로그 파일 경로에 쓰기 권한이 없을 때. |

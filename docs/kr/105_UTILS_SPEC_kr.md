# 유틸리티 모듈 명세 (Utils Module Specification)

## 1. 개요 (Overview)
본 문서는 `src/utils/`에 위치한 핵심 유틸리티 모듈을 정의합니다. 이 모듈들은 **로깅(Logging)**, **비용 추적(Cost Tracking)**, **데코레이터(Decorators)**, **프롬프트 관리(Prompt Management)**와 같은 공통 관심사(Cross-cutting Concerns)를 처리합니다.

---

## 2. Logger (`src/utils/logger.py`)

### 2.1. 개요
**Singleton Pattern**을 사용하여 애플리케이션 전역에서 일관된 포맷의 로그를 관리합니다.

### 2.2. 시그니처 (Signature)
```python
class LoggerManager:
    @staticmethod
    def get_instance() -> 'LoggerManager': ...
    def get_logger(self) -> logging.Logger: ...
```

### 2.3. 동작 로직 (Behavior Logic)
1.  **싱글톤 확인**: `get_instance()` 호출 시 `_instance` 존재 여부를 확인하고, 없으면 스레드 안전(Thread-safe)하게 생성합니다.
2.  **설정**: 초기화 시 로그 레벨(INFO/DEBUG), 포맷(KST 타임스탬프), 핸들러(콘솔/파일)를 설정합니다.
3.  **전역 후킹**: `sys.excepthook`을 등록하여 처리되지 않은 예외를 전역적으로 포착하고 로깅합니다.

### 2.4. 사용 예시 (Usage Example)
```python
from src.utils.logger import LoggerManager

logger = LoggerManager.get_instance().get_logger()
logger.info("System initialized")
```

---

## 3. Callbacks (`src/utils/callbacks.py`)

### 3.1. 개요
LangChain의 생명주기 이벤트(`on_llm_end`)에 훅(Hook)을 걸어 토큰 사용량과 비용을 계산하고 기록합니다.

### 3.2. 시그니처 (Signature)
```python
class CostCallbackHandler(BaseCallbackHandler):
    def __init__(self, log_path: str = "logs/cost.jsonl"): ...
    def on_llm_end(self, response: LLMResult, **kwargs) -> None: ...
```

### 3.3. 동작 로직 (Behavior Logic)
1.  **이벤트 트리거**: LLM 호출이 완료되면 자동으로 트리거됩니다.
2.  **토큰 추출**: `LLMResult`를 파싱하여 `token_usage`를 찾습니다 (OpenAI/Anthropic 등 제공자별 포맷 대응).
3.  **비용 계산**: `SUPPORTED_MODELS`에서 단가를 조회하여 `(입력 토큰 * 입력 단가) + (출력 토큰 * 출력 단가)`를 계산합니다.
4.  **로깅**: 계산된 비용 정보를 JSON 레코드로 `log_path`에 추가(Append)합니다.

### 3.4. 사용 예시 (Usage Example)
```python
handler = CostCallbackHandler()
llm.invoke("Hi", callbacks=[handler])
```

---

## 4. Decorators (`src/utils/decorators.py`)

### 4.1. 개요
반복적인 코드를 줄이기 위해 `CostCallbackHandler` 같은 의존성을 자동으로 주입합니다.

### 4.2. 시그니처 (Signature)
```python
def measure_cost(func: Callable) -> Callable: ...
```

### 4.3. 동작 로직 (Behavior Logic)
1.  **가로채기 (Interception)**: 대상 함수를 래핑합니다.
2.  **주입 (Injection)**: `kwargs`의 `callbacks` 인자를 검사하여, 없거나 비어 있으면 새로운 `CostCallbackHandler`를 주입합니다.
3.  **실행 (Execution)**: 수정된 인자로 원본 함수를 실행합니다.

### 4.4. 사용 예시 (Usage Example)
```python
@measure_cost
def run_chat(prompt, callbacks=None):
    return llm.invoke(prompt, callbacks=callbacks)
```

---

## 5. Prompt Manager (`src/utils/prompt_manager.py`)

### 5.1. 개요
파일 시스템에서 YAML 기반의 프롬프트 템플릿을 로드하고 관리합니다.

### 5.2. 시그니처 (Signature)
```python
class PromptManager:
    def load_template(self, file_name: str, key: str = "template") -> str: ...
```

### 5.3. 동작 로직 (Behavior Logic)
1.  **경로 해석**: `src/prompts/templates/`를 기준으로 `file_name`의 경로를 해석합니다.
2.  **파일 읽기**: UTF-8 인코딩으로 파일을 엽니다. 파일이 없으면 `FileNotFoundError`를 발생시킵니다.
3.  **파싱**: YAML 내용을 파싱합니다. 문법 오류 시 `YAMLError`를 발생시킵니다.
4.  **키 추출**: 지정된 `key`의 값을 반환합니다. 키가 없으면 `KeyError`를 발생시킵니다.

### 5.4. 사용 예시 (Usage Example)
```python
manager = PromptManager()
system_prompt = manager.load_template("nfc_character.yaml", key="system_prompt")
```

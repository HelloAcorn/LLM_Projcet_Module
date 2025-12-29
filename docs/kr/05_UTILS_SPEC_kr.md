# Utils Module Specification (유틸리티 모듈 명세)

## 1. 개요 (Overview)
본 문서는 `src/utils/` 디렉토리에 위치한 공통 유틸리티 모듈들의 기능, 인터페이스 및 구현 요구사항을 정의합니다. 이 모듈들은 로깅, 비용 추적, 프롬프트 관리 등 시스템 전반에서 재사용되는 핵심 기능을 제공합니다.

## 2. Logger (`src/utils/logger.py`)

### 2.1. 목적
- 애플리케이션 전반의 로그를 일관된 포맷으로 출력 및 관리합니다.
- Singleton 패턴을 통해 단일 인스턴스를 유지합니다.

### 2.2. 주요 기능
- **Singleton Pattern**: `LoggerManager`를 통해 시스템 내 유일한 로거 인스턴스 보장.
- **Console Formatting**: 레벨별 색상 구분 및 KST(한국 표준시) 기준 타임스탬프 적용.
- **Global Exception Hook**: 처리되지 않은 예외(Uncaught Exception)를 자동으로 포착하여 로깅.

### 2.3. 인터페이스
```python
logger = LoggerManager.get_instance().get_logger()
logger.info("메시지")
logger.error("에러 메시지")
```

## 3. Callbacks (`src/utils/callbacks.py`)

### 3.1. 목적
- LangChain 기반 LLM 호출의 생명주기 이벤트를 훅(Hook)하여 토큰 사용량과 비용을 추적합니다.

### 3.2. 주요 기능
- **Cost Tracking**: `on_llm_end` 이벤트 발생 시 토큰 사용량 추출.
- **Universal Token Extraction**: OpenAI, Anthropic, Gemini 등 다양한 프로바이더의 응답 포맷(llm_output, generation_info, message metadata)을 자동으로 파싱.
- **Pricing Calculation**: `02_LLM_FACTORY_SPEC`에 정의된 모델별 단가를 기준으로 비용 계산.
- **Logging**: 계산된 비용 정보를 `logs/cost.jsonl` 파일에 JSON 형식으로 기록.

### 3.3. 인터페이스
```python
handler = CostCallbackHandler(log_path="logs/cost.jsonl")
# LangChain 모델 호출 시 callbacks 인자로 전달
```

## 4. Decorators (`src/utils/decorators.py`)

### 4.1. 목적
- 함수 호출 시 반복적으로 사용되는 `CostCallbackHandler` 주입 로직을 간소화합니다.

### 4.2. 주요 기능
- **`@measure_cost`**: 대상 함수의 `callbacks` 인자를 검사하여 `CostCallbackHandler`가 없으면 자동으로 주입합니다.

### 4.3. 사용 예시
```python
@measure_cost
def invoke_llm(prompt, callbacks=[]):
    return llm.invoke(prompt, callbacks=callbacks)
```

## 5. Prompt Manager (`src/utils/prompt_manager.py`)

### 5.1. 목적
- YAML 파일 기반의 프롬프트 템플릿을 로드하고 관리합니다.

### 5.2. 주요 기능
- **YAML Loading**: 지정된 경로의 YAML 파일을 UTF-8 인코딩으로 읽어옵니다.
- **Key Validation**: 특정 키(기본값: `template`)의 존재 여부를 검증합니다.
- **Error Handling**: 파일 부재(`FileNotFoundError`) 및 키 누락(`KeyError`) 시 명시적 예외 발생.

### 5.3. 인터페이스
```python
# 단일 템플릿 로드
template_str = load_prompt("path/to/prompt.yaml", key="template")

# 전체 YAML 로드
config = load_yaml("path/to/config.yaml")
```


# 프롬프트 매니저 명세 (Prompt Manager Specification)

## 1. 개요 (Overview)
본 모듈(`src.utils.prompt_manager`)은 파일 시스템에서 YAML 기반의 프롬프트 템플릿을 로드하는 유틸리티 함수들을 제공합니다. 정적인 프롬프트 리소스를 관리하는 통일된 인터페이스 역할을 합니다.

## 2. 파일 경로 (File Path)
- `src/utils/prompt_manager.py`

## 3. 의존성 (Dependencies)
- **External**: `yaml` (PyYAML), `pathlib`
- **Internal**: 없음

## 4. 함수 시그니처 (Function Signature)

### 4.1. `load_prompt`
YAML 파일에서 특정 키(기본값: "template")의 값을 로드합니다.

```python
def load_prompt(yaml_path: str, key: str = "template") -> Any:
    """YAML 템플릿 파일에서 특정 키의 값을 로드합니다."""
    ...
```

### 4.2. `load_yaml`
YAML 파일의 전체 내용을 딕셔너리로 로드합니다.

```python
def load_yaml(yaml_path: str) -> Dict[str, Any]:
    """전체 YAML 파일을 로드합니다."""
    ...
```

## 5. 동작 로직 (Behavior Logic)

### 5.1. `load_prompt`
1.  **경로 검증**: 입력된 `yaml_path` 문자열을 `Path` 객체로 변환하고 `.exists()`로 파일 존재 여부를 확인합니다.
2.  **예외 처리 (파일)**: 파일이 없으면 즉시 `FileNotFoundError`를 발생시킵니다.
3.  **파일 읽기**: `utf-8` 인코딩으로 파일을 열고 `yaml.safe_load`를 사용하여 파싱합니다.
4.  **키 검증**: 파싱된 딕셔너리에 요청된 `key`가 존재하는지 확인합니다.
5.  **예외 처리 (키)**: 키가 없으면 `KeyError`를 발생시킵니다.
6.  **반환**: 키에 해당하는 값을 반환합니다.

### 5.2. `load_yaml`
1.  **경로 변환**: `yaml_path`를 `Path` 객체로 변환합니다.
2.  **파일 읽기**: `utf-8` 인코딩으로 파일을 열고 `yaml.safe_load`로 파싱합니다.
3.  **반환**: 전체 딕셔너리 객체를 반환합니다.

## 6. 사용 예시 (Usage Example)

```python
from src.utils.prompt_manager import load_prompt, load_yaml

# Case 1: 특정 프롬프트 문자열 로드
try:
    system_prompt = load_prompt("src/prompts/templates/nfc_character.yaml", key="system_prompt")
    print(system_prompt)
except FileNotFoundError as e:
    print(e)

# Case 2: 전체 설정 로드
config = load_yaml("src/core/config.yaml")
print(config)
```

## 7. 에러 처리 (Error Handling)

| 예외 (Exception) | 발생 조건 (Condition) |
|---|---|
| `FileNotFoundError` | 지정된 YAML 파일 경로가 존재하지 않을 때. |
| `KeyError` | YAML 데이터 내에 요청된 `key`가 없을 때 (`load_prompt` 전용). |
| `YAMLError` | YAML 파일 문법이 잘못되었을 때 (`PyYAML`에서 전파). |


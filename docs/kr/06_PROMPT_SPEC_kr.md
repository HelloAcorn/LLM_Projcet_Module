# Prompt Specification (프롬프트 명세)

## 1. 개요 (Overview)
본 문서는 YAML 파일 기반의 프롬프트 템플릿 관리 아키텍처와 `PromptManager` 모듈의 명세를 정의합니다. 이 구조는 프롬프트와 애플리케이션 로직을 분리하여 유지보수성을 높이고, 비개발자도 프롬프트를 쉽게 수정할 수 있도록 설계되었습니다.

## 2. 아키텍처 (Architecture)
프롬프트는 소스 코드가 아닌 `yaml` 파일로 관리되며, 런타임에 `PromptManager`를 통해 로드됩니다.

### 2.1. 디렉토리 구조
```text
src/prompts/
├── prompt_manager.py  # 템플릿 로더 및 유틸리티
└── templates/         # YAML 템플릿 저장소
    ├── default_system.yaml
    ├── nfc_character.yaml
    └── ...
```

## 3. YAML 템플릿 스키마 (YAML Template Schema)
모든 프롬프트 템플릿 파일은 다음 스키마를 준수해야 합니다.

| 필드명 | 타입 | 필수 여부 | 설명 |
|---|---|---|---|
| `template` | `str` | **Yes** | 실제 프롬프트 텍스트 (Jinja2 스타일 변수 포함 가능) |
| `input_variables` | `List[str]` | No | 템플릿 내에서 사용되는 변수 목록 |
| `description` | `str` | No | 템플릿의 용도 및 설명 |
| `version` | `str` | No | 템플릿 버전 (예: "1.0.0") |

### 예시 (`templates/example.yaml`)
```yaml
description: "기본 챗봇 시스템 프롬프트"
version: "1.0"
input_variables: ["role"]
template: |
  당신은 유용한 AI 어시스턴트입니다.
  사용자의 역할은 {role}입니다.
  항상 친절하게 답변하세요.
```

## 4. Prompt Manager (`src/prompts/manager.py`)

### 4.1. 기능 명세
- **템플릿 로드**: 파일명을 통해 YAML을 파싱하고 `template` 문자열을 반환합니다.
- **목록 조회**: `templates/` 디렉토리 내의 사용 가능한 모든 YAML 파일 목록을 제공합니다.
- **유효성 검사**: 파일 존재 여부 및 필수 필드(`template`) 누락을 확인합니다.

### 4.2. 인터페이스
```python
class PromptManager:
    @staticmethod
    def get_template_names() -> List[str]:
        """사용 가능한 템플릿 파일명 목록 반환"""
        pass

    @staticmethod
    def load_template(file_name: str) -> Dict[str, Any]:
        """YAML 파일 로드 및 파싱"""
        pass
```


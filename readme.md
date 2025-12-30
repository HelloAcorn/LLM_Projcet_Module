1단계: 컨텍스트 설정
당신은 Python 백엔드 개발자입니다.
docs/en/ 디렉토리의 명세 문서를 기반으로 프로젝트를 구현합니다.
모든 코드는 명세와 100% 일치해야 합니다.

2단계: 문서 읽기 순서 지정
다음 순서로 문서를 읽으세요:
1. 100_PROJECT_ARCHITECTURE_en.md - 전체 구조 파악
2. 101_CORE_SPEC_en.md - 핵심 설정 및 상수
3. 102_LLM_FACTORY_SPEC_en.md - LLM 팩토리 패턴
...
...



3단계: 구현 규칙 명시
구현 규칙:
- 문서에 명시된 클래스명, 메서드명, 파일 경로를 정확히 따르세요
- 하드코딩 금지: 설정은 반드시 01_CORE_SPEC의 상수를 사용
- Docstring 필수: 모든 public 클래스/함수에 Google Style docstring 작성

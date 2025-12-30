# 어드민 콘솔 명세 (Admin Console Specification)

## 1. 개요 (Overview)
본 모듈(`streamlit/admin.py`)은 Streamlit 기반의 통합 대시보드입니다. 시스템의 **관측성(Observability)**을 확보하고, LLM 프롬프트를 실시간으로 실험할 수 있는 **Playground** 환경을 제공합니다.

## 2. 파일 경로 (File Path)
- `streamlit/admin.py`

## 3. 의존성 (Dependencies)
- **External**: `streamlit`, `pandas`, `plotly`, `json`, `sys`, `pathlib`
- **Internal**: `src.llm.llm_factory`, `src.utils.callbacks`

## 4. 페이지 구성 (Page Configuration)
- **Title**: AI Service Admin Console
- **Icon**: 🛠️
- **Layout**: Wide Mode

## 5. 기능 명세 (Functional Specification)

### 5.1. 대시보드 (Dashboard)
시스템의 경제적, 기술적 성능 지표를 시각화합니다.
- **데이터 소스**:
    -   비용 로그: `logs/cost.jsonl`
    -   API 로그: `logs/api_requests.jsonl`
- **주요 지표 (Metrics)**:
    -   총 추정 비용 ($), 총 사용 토큰 수, 총 LLM 호출 횟수.
- **시각화 (Visualizations)**:
    -   **Daily Cost**: 일별/모델별 비용 추이 (Bar Chart).
    -   **Model Usage**: 모델별 호출 빈도 (Pie Chart).
    -   **API Performance**: 엔드포인트별 요청 수, 평균/P95 레이턴시, 성공률 테이블.

### 5.2. 플레이그라운드 (Playground)
개발자가 프롬프트를 테스트하고 즉각적인 피드백을 받을 수 있는 샌드박스입니다.
- **설정 (Settings)**:
    -   **Model**: `SUPPORTED_MODELS` 목록에서 선택 (OpenAI, Anthropic, Gemini).
    -   **Temperature**: 슬라이더로 조절 (0.0 ~ 1.0).
- **템플릿 매니저 (Template Manager)**:
    -   `src/prompts/templates/` 디렉토리의 YAML/Text 파일을 로드하여 System Prompt에 적용.
- **채팅 인터페이스 (Chat Interface)**:
    -   System Prompt 편집기: 페르소나 및 규칙 실시간 수정.
    -   Chat Input/Output: `LLMFactory`를 통한 실시간 대화 및 스트리밍 응답.
    -   **이력 다운로드**: 현재 대화 내용을 JSON 파일로 로컬에 저장.

## 6. 동작 로직 (Behavior Logic)

1.  **초기화 (Initialization)**:
    -   `sys.path`에 프로젝트 루트와 `src`를 추가하여 모듈 임포트 경로를 확보합니다.
    -   `os.makedirs`로 로그 및 프롬프트 디렉토리 존재를 보장합니다.
2.  **데이터 로딩 (Data Loading)**:
    -   `cost.jsonl`과 `api_requests.jsonl`을 Pandas DataFrame으로 로드합니다. 파일이 없거나 손상된 경우 빈 DataFrame을 반환하여 크래시를 방지합니다.
3.  **LLM 실행 (Invocation)**:
    -   사용자 입력 시 `LLMFactory.create()`로 인스턴스를 생성합니다.
    -   `invoke()` 결과를 받아 구조화된 출력(JSON)과 원시 출력(Raw)을 파싱합니다.
    -   `response_metadata` 또는 `usage_metadata`에서 토큰 사용량을 추출하여 실시간 비용을 계산하고 로그 파일에 추가(Append)합니다.

## 7. 실행 (Execution)
```bash
streamlit run streamlit/admin.py
```


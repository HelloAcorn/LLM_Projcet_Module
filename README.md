# LLM Project Module

범용 Prompt Engineering 및 RAG 프로젝트를 위한 재사용 가능한 기본 골격 프로젝트

## 프로젝트 개요

이 프로젝트는 다양한 LLM 기반 애플리케이션(프롬프트 엔지니어링, RAG, 에이전트 등)을 빠르게 개발할 수 있도록 설계된 범용 모듈입니다. 추상화된 인터페이스를 통해 벤더 독립적이며, 확장 가능한 구조를 제공합니다.

## 핵심 설계 원칙

1. **모듈화**: 각 컴포넌트를 독립적으로 교체/확장 가능
2. **추상화**: 인터페이스 기반 설계로 다양한 LLM/벡터DB 지원
3. **재사용성**: 다른 프로젝트에서 즉시 활용 가능
4. **확장성**: 새로운 기능 추가가 용이한 구조
5. **프로덕션 준비**: 로깅, 캐싱, 비용 추적 내장

## 디렉토리 구조

```
LLM_Project_Module/
├── run_app.py                  # 메인 실행 스크립트
├── pyproject.toml              # 프로젝트 설정 (Poetry/UV)
├── config.yaml                 # 기본 설정 파일
├── .env.example                # 환경 변수 템플릿
├── README.md                   # 문서
├── app/
│   ├── core/                   # 핵심 추상화 레이어
│   │   ├── base_llm.py         # LLM 인터페이스
│   │   ├── base_embedder.py    # 임베딩 모델 인터페이스
│   │   ├── base_vectorstore.py # 벡터 DB 인터페이스
│   │   ├── base_retriever.py   # 검색기 인터페이스
│   │   ├── base_prompt.py      # 프롬프트 템플릿 인터페이스
│   │   ├── llm_factory.py      # LLM 생성 팩토리
│   │   └── settings.py         # 전역 설정 관리
│   │
│   ├── llm/                    # LLM 구현체
│   │   ├── openai_llm.py       # OpenAI GPT
│   │   ├── anthropic_llm.py    # Claude
│   │   ├── local_llm.py        # vLLM/Ollama
│   │   └── google_llm.py       # Gemini
│   │
│   ├── embeddings/             # 임베딩 모델 구현체
│   │   ├── openai_embedder.py  # text-embedding-3
│   │   ├── huggingface_embedder.py  # BGE/E5
│   │   └── cohere_embedder.py  # Cohere Embed
│   │
│   ├── vectorstore/            # 벡터 DB 구현체
│   │   ├── faiss_store.py      # FAISS
│   │   ├── chroma_store.py     # ChromaDB
│   │   ├── qdrant_store.py     # Qdrant
│   │   └── pinecone_store.py   # Pinecone
│   │
│   ├── retrieval/              # RAG 검색 전략
│   │   ├── dense_retriever.py  # 밀집 벡터 검색
│   │   ├── hybrid_retriever.py # Hybrid (Dense + Sparse)
│   │   ├── reranker.py         # Re-ranking (Cohere, BGE)
│   │   └── query_expander.py   # 쿼리 확장/변환
│   │
│   ├── prompts/                # 프롬프트 관리
│   │   ├── templates/          # 프롬프트 템플릿
│   │   │   ├── qa.yaml         # Q&A 템플릿
│   │   │   ├── summarization.yaml
│   │   │   ├── analysis.yaml
│   │   │   └── custom.yaml
│   │   ├── prompt_manager.py   # 템플릿 로드/관리
│   │   ├── prompt_optimizer.py # 프롬프트 최적화
│   │   └── few_shot_manager.py # Few-shot 예시 관리
│   │
│   ├── agents/                 # 에이전트 & 체인 시스템
│   │   ├── chains/             # 실행 체인/파이프라인
│   │   │   ├── base_chain.py   # 체인 인터페이스
│   │   │   ├── simple_chain.py # 단순 LLM 체인
│   │   │   ├── rag_chain.py    # RAG 파이프라인
│   │   │   ├── multi_query_chain.py # 멀티 쿼리 RAG
│   │   │   └── sequential_chain.py  # 순차 체인
│   │   │
│   │   ├── base_agent.py       # 에이전트 인터페이스
│   │   ├── react_agent.py      # ReAct 패턴
│   │   ├── plan_execute_agent.py   # Plan & Execute 패턴
│   │   ├── reflection_agent.py     # Reflection 패턴
│   │   ├── tool_executor.py    # 도구 실행기
│   │   ├── agent_memory.py     # 에이전트 메모리 관리
│   │   └── tools/              # 에이전트 도구
│   │       ├── base_tool.py    # 도구 인터페이스
│   │       ├── search_tool.py  # 검색 도구
│   │       ├── calculator_tool.py  # 계산 도구
│   │       ├── rag_tool.py     # RAG 도구
│   │       └── custom_tool.py  # 커스텀 도구
│   │
│   ├── data/                   # 데이터 처리
│   │   ├── loader.py           # 문서 로더 (PDF, TXT, JSON 등)
│   │   ├── splitter.py         # 텍스트 분할기
│   │   ├── preprocessor.py     # 전처리 파이프라인
│   │   ├── logger.py           # 로그 작성
│   │   └── indexer.py          # 인덱싱 관리
│   │
│   └── utils/                  # 유틸리티
│       ├── logger.py           # 로깅 설정
│       ├── cache.py            # 캐싱 (Redis/로컬)
│       ├── rate_limiter.py     # API 속도 제한
│       ├── cost_tracker.py     # 비용 추적
│       ├── yaml_manager.py     # YAML 파일 관리
│       └── visualizer.py       # 시각화 도구
│
├── examples/                   # 사용 예시
│   ├── simple_prompt.py        # 기본 프롬프트 실행
│
├── tests/                      # 테스트
│   ├── unit/                   # 단위 테스트
│   ├── integration/            # 통합 테스트
│   └── fixtures/               # 테스트 데이터
│
└── logs/                       # 실행 로그
    ├── app.log
    └── cost.log

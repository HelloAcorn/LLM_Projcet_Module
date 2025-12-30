# Test Strategy Specification

## 1. Overview
본 프로젝트는 3가지 테스트 전략을 사용합니다:
- **Sociable Unit Test**: 실제 의존성 사용, 외부 API만 Mock
- **Broad Integration Test**: 전체 파이프라인 검증
- **Contract Testing**: API 스펙 준수 검증

---

## 2. Sociable Unit Test

### 목적
모듈 내부 로직을 실제 의존성과 함께 검증

### 규칙
- 실제 클래스 인스턴스 사용
- 외부 API/DB만 Mock
- AAA 패턴 (Arrange-Act-Assert)

### 예시
```python
# tests/unit/test_prompt_manager.py
def test_load_template():
    # Arrange
    manager = PromptManager()
    
    # Act
    result = manager.load_template("default_system")
    
    # Assert
    assert "template" in result
    assert isinstance(result["template"], str)
```

---

## 3. Broad Integration Test

### 목적
여러 모듈이 함께 동작하는 전체 흐름 검증

### 규칙
- 실제 모듈 간 통합
- 외부 API만 Mock
- `@pytest.mark.integration` 표시

### 예시
```python
# tests/integration/test_chat_pipeline.py
@pytest.mark.integration
def test_full_chat_flow():
    # PromptManager + LLMFactory + Callback 통합
    template = PromptManager().load_template("default")
    callback = CostCallbackHandler()
    
    with patch('langchain_openai.ChatOpenAI') as mock:
        mock.return_value.invoke.return_value = Mock(content="response")
        llm = LLMFactory.create("openai", callbacks=[callback])
        
        response = llm.invoke(template["template"])
        
        assert response.content == "response"
        assert callback.total_cost > 0
```

---

## 4. Contract Testing

### 목적
API가 명세를 준수하는지 검증

### 규칙
- HTTP 상태 코드 검증
- 요청/응답 스키마 검증
- API 문서와 100% 일치

### 예시
```python
# tests/integration/test_api_contract.py
def test_chat_endpoint():
    response = client.post("/chat", json={
        "provider": "openai",
        "messages": [{"role": "user", "content": "Hi"}]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "cost" in data
    assert isinstance(data["cost"], float)

def test_invalid_provider():
    response = client.post("/chat", json={
        "provider": "invalid"
    })
    
    assert response.status_code == 422
```

---

## 5. Test Structure
```
tests/
├── unit/                    # Sociable Unit Tests
│   ├── test_llm_factory.py
│   └── test_prompt_manager.py
├── integration/             # Integration + Contract
│   ├── test_chat_pipeline.py
│   └── test_api_contract.py
└── conftest.py              # 공통 Fixtures
```

---

## 6. Execution
```bash
# Unit 테스트
pytest tests/unit/

# Integration 테스트
pytest tests/integration/ -m integration

# 전체 + Coverage
pytest --cov=src --cov-report=html
```

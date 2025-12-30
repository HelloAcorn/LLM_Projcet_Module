# Test Strategy Specification

## 1. Overview
This project uses three testing strategies:
- **Sociable Unit Test**: Uses real dependencies, mocking only external APIs.
- **Broad Integration Test**: Verifies the entire pipeline.
- **Contract Testing**: Verifies API specification compliance.

---

## 2. Sociable Unit Test

### Purpose
Verify internal module logic alongside real dependencies.

### Rules
- Use real class instances.
- Mock only external APIs/DBs.
- Follow the AAA pattern (Arrange-Act-Assert).

### Example
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

### Purpose
Verify the full flow where multiple modules operate together.

### Rules
- Integrate real modules.
- Mock only external APIs.
- Mark with `@pytest.mark.integration`.

### Example
```python
# tests/integration/test_chat_pipeline.py
@pytest.mark.integration
def test_full_chat_flow():
    # Integrate PromptManager + LLMFactory + Callback
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

### Purpose
Verify that the API complies with the specifications.

### Rules
- Verify HTTP status codes.
- Verify request/response schemas.
- Must match 100% with API documentation.

### Example
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
└── conftest.py              # Common Fixtures
```

---

## 6. Execution
```bash
# Unit Tests
pytest tests/unit/

# Integration Tests
pytest tests/integration/ -m integration

# Full + Coverage
pytest --cov=src --cov-report=html
```

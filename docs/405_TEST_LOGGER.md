# Logger Test Specification

## 1. Overview
Tests the `src.utils.logger.LoggerManager` for singleton properties and correct logging configuration.

## 2. Target Component
- **Component**: `src.utils.logger.LoggerManager`
- **Spec Document**: `docs/105_UTILS_LOGGER.md`

## 3. Test Cases (Unit)

### 3.1. Singleton Property
- **Scenario**: Verify only one instance exists.
- **Input**: Call `LoggerManager.get_instance()` multiple times.
- **Expected Output**: `instance1 is instance2` should be True.

### 3.2. Logger Configuration
- **Scenario**: Check if handlers are attached.
- **Input**: `get_logger()`.
- **Expected Output**: Logger should have at least one `StreamHandler` (or `FileHandler`).

### 3.3. Exception Hook
- **Scenario**: Verify `sys.excepthook` is overridden.
- **Input**: Check `sys.excepthook`.
- **Expected Output**: Should point to `LoggerManager`'s hook method, not the default.

## 4. Test Implementation Plan
- **File**: `tests/unit/test_logger.py`
- **Tools**: `pytest`.


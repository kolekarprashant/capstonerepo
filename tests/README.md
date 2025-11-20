# Tests

This directory contains test files for the project using pytest.

## Running Tests

To run all tests:
```bash
pytest
```

To run tests with verbose output:
```bash
pytest -v
```

To run a specific test file:
```bash
pytest tests/test_api.py
```

To run tests and show print statements:
```bash
pytest -s
```

To run tests with coverage:
```bash
pytest --cov=API --cov-report=html
```

## Test Structure

- `test_api.py` - Basic tests demonstrating pytest functionality
- `conftest.py` - Pytest configuration and shared fixtures

## Writing Tests

Test files should:
- Be named `test_*.py`
- Have test functions named `test_*()`
- Use assertions to validate behavior

Example:
```python
def test_example():
    assert 1 + 1 == 2
```

## Dependencies

The following testing dependencies are required (installed via requirements.txt):
- pytest==8.3.4
- pytest-asyncio==0.25.2
- httpx==0.28.1

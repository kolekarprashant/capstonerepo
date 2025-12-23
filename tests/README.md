# Test Suite

This directory contains the test suite for the FastAPI application.

## Prerequisites

Install the required testing dependencies:

```bash
pip install pytest pytest-asyncio httpx python-multipart
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run tests with verbose output
```bash
pytest tests/ -v
```

### Run a specific test file
```bash
pytest tests/test_api.py
```

### Run a specific test class
```bash
pytest tests/test_api.py::TestHomeEndpoint
```

### Run a specific test
```bash
pytest tests/test_api.py::TestHomeEndpoint::test_home_endpoint
```

## Test Coverage

The test suite covers the following API endpoints:

1. **Home Endpoint (`GET /`)**
   - Tests basic server functionality

2. **Extract Image Endpoint (`POST /extract-image`)**
   - Tests image upload and text extraction

3. **RAG PDF Endpoint (`POST /rag-pdf`)**
   - Tests PDF question-answering functionality

4. **Text-to-SQL Endpoint (`POST /text-sql`)**
   - Tests SQL query generation from natural language
   - Tests with and without session management

5. **Report Endpoint (`POST /report`)**
   - Tests report generation functionality

6. **Error Handling**
   - Tests invalid endpoints return 404
   - Tests missing parameters return 422

7. **CORS Configuration**
   - Tests CORS headers are properly set

## Test Structure

Tests are organized into classes by functionality:
- `TestHomeEndpoint` - Home endpoint tests
- `TestExtractImageEndpoint` - Image extraction tests
- `TestRagPdfEndpoint` - RAG PDF tests
- `TestTextSqlEndpoint` - Text-to-SQL tests
- `TestReportEndpoint` - Report generation tests
- `TestCORSConfiguration` - CORS configuration tests
- `TestInvalidRequests` - Error handling tests

## Mocking

The tests use mocking to isolate API endpoint logic from external dependencies:
- Service functions are mocked to avoid requiring real API keys
- External API calls are mocked to ensure fast, reliable tests
- File uploads are simulated with test data

## Notes

- Tests use `TestClient` from FastAPI for HTTP testing
- All tests run independently and can be executed in any order
- Mock environment variables are set for testing purposes

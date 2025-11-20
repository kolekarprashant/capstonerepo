"""
Pytest configuration and fixtures
"""
import os
import pytest

# Set up environment variables for testing
os.environ.setdefault('CO_API_KEY', 'test-cohere-key')
os.environ.setdefault('OPENAI_API_KEY', 'test-openai-key')
os.environ.setdefault('AWS_ACCESS_KEY_ID', 'test-aws-key')
os.environ.setdefault('AWS_SECRET_ACCESS_KEY', 'test-aws-secret')


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables before all tests"""
    # This runs before all tests
    yield
    # Cleanup after all tests (if needed)

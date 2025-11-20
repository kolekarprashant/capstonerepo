"""
Basic test to verify pytest is accessible and working
"""
import pytest


def test_pytest_is_accessible():
    """Test that pytest is accessible and working"""
    assert True


def test_basic_math():
    """Test basic mathematical operations"""
    assert 1 + 1 == 2
    assert 2 * 3 == 6
    assert 10 / 2 == 5


def test_string_operations():
    """Test string operations"""
    test_string = "pytest is accessible"
    assert "pytest" in test_string
    assert test_string.startswith("pytest")
    assert len(test_string) > 0


@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
])
def test_parametrized_multiplication(input, expected):
    """Test parametrized test functionality"""
    assert input * 2 == expected

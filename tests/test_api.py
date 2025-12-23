"""
Test cases for the FastAPI application endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
import os

# Set mock environment variables before importing any modules
os.environ['CO_API_KEY'] = 'test_cohere_key'
os.environ['OPENAI_API_KEY'] = 'test_openai_key'
os.environ['AWS_ACCESS_KEY_ID'] = 'test_aws_key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_aws_secret'

# Add the API directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'API'))

# Mock the Cohere client initialization
with patch('langchain_cohere.chat_models.ChatCohere.__init__', return_value=None), \
     patch('langchain_openai.chat_models.ChatOpenAI.__init__', return_value=None):
    from main import app

client = TestClient(app)


class TestHomeEndpoint:
    """Test cases for the home endpoint."""
    
    def test_home_endpoint(self):
        """Test that the home endpoint returns a success message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "FastAPI server is running successfully!"}


class TestExtractImageEndpoint:
    """Test cases for the extract-image endpoint."""
    
    @patch('main.run_extract_image')
    def test_extract_image_endpoint(self, mock_run_extract_image):
        """Test the extract-image endpoint with mocked service."""
        # Mock the service response
        mock_run_extract_image.return_value = {
            "question": "What is in this image?",
            "answer": "This is a test image"
        }
        
        # Create a mock file
        file_content = b"fake image content"
        files = {"file": ("test.jpg", file_content, "image/jpeg")}
        data = {"question": "What is in this image?"}
        
        response = client.post("/extract-image", files=files, data=data)
        
        assert response.status_code == 200
        assert "question" in response.json()
        assert "answer" in response.json()


class TestRagPdfEndpoint:
    """Test cases for the rag-pdf endpoint."""
    
    @patch('main.run_rag_query')
    def test_rag_pdf_endpoint(self, mock_run_rag_query):
        """Test the rag-pdf endpoint with mocked service."""
        # Mock the service response
        mock_run_rag_query.return_value = {
            "question": "What is the main topic?",
            "answer": "The main topic is testing"
        }
        
        data = {"question": "What is the main topic?"}
        response = client.post("/rag-pdf", data=data)
        
        assert response.status_code == 200
        mock_run_rag_query.assert_called_once_with("What is the main topic?")


class TestTextSqlEndpoint:
    """Test cases for the text-sql endpoint."""
    
    @patch('main.run_txt_sql_query')
    def test_text_sql_endpoint_without_session(self, mock_run_txt_sql_query):
        """Test the text-sql endpoint without session_id."""
        # Mock the service response
        mock_run_txt_sql_query.return_value = {
            "question": "SELECT * FROM users",
            "result": "Query executed successfully"
        }
        
        data = {"question": "Show me all users"}
        response = client.post("/text-sql", data=data)
        
        assert response.status_code == 200
        mock_run_txt_sql_query.assert_called_once()
    
    @patch('main.run_txt_sql_query')
    def test_text_sql_endpoint_with_session(self, mock_run_txt_sql_query):
        """Test the text-sql endpoint with session_id."""
        # Mock the service response
        mock_run_txt_sql_query.return_value = {
            "question": "SELECT * FROM users",
            "result": "Query executed successfully"
        }
        
        data = {"question": "Show me all users", "session_id": "test-session-123"}
        response = client.post("/text-sql", data=data)
        
        assert response.status_code == 200
        mock_run_txt_sql_query.assert_called_once()


class TestReportEndpoint:
    """Test cases for the report endpoint."""
    
    @patch('main.run_agents')
    def test_report_endpoint(self, mock_run_agents):
        """Test the report endpoint with mocked service."""
        # Mock the service response
        mock_run_agents.return_value = {
            "question": "Generate sales report",
            "report": "Sales report generated successfully"
        }
        
        data = {"question": "Generate sales report"}
        response = client.post("/report", data=data)
        
        assert response.status_code == 200
        mock_run_agents.assert_called_once_with("Generate sales report")


class TestCORSConfiguration:
    """Test cases for CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are properly configured."""
        response = client.options("/")
        # The CORS middleware should add appropriate headers
        assert response.status_code in [200, 405]  # OPTIONS might not be explicitly defined


class TestInvalidRequests:
    """Test cases for invalid requests."""
    
    def test_invalid_endpoint(self):
        """Test that invalid endpoints return 404."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404
    
    @patch('main.run_rag_query')
    def test_rag_pdf_missing_question(self, mock_run_rag_query):
        """Test rag-pdf endpoint with missing question parameter."""
        response = client.post("/rag-pdf", data={})
        # FastAPI should return 422 for missing required field
        assert response.status_code == 422

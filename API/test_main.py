import os, sys, pytest
from fastapi.testclient import TestClient
# Ensure imports work when running pytest from repo root
sys.path.append(os.path.dirname(__file__))
import main as main_module
from main import app

client = TestClient(app)


def test_home():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "FastAPI server is running successfully!"}


def test_extract_image(monkeypatch, tmp_path):
    async def fake_run_extract_image(file, question):
        return {"question": question, "answer": "stubbed-image-answer"}

    monkeypatch.setattr(main_module, "run_extract_image", fake_run_extract_image)

    file_content = b"fake-binary"
    files = {"file": ("test.png", file_content, "image/png")}
    data = {"question": "What is in the image?"}
    resp = client.post("/extract-image", files=files, data=data)
    assert resp.status_code == 200
    assert resp.json()["answer"] == "stubbed-image-answer"


def test_rag_pdf(monkeypatch):
    def fake_run_rag_query(question: str):
        return {"question": question, "answer": "stubbed-rag-answer"}

    monkeypatch.setattr(main_module, "run_rag_query", fake_run_rag_query)

    resp = client.post("/rag-pdf", data={"question": "Some question"})
    assert resp.status_code == 200
    assert resp.json()["answer"] == "stubbed-rag-answer"


def test_text_sql(monkeypatch):
    def fake_run_txt_sql_query(session_id, memory_store, question):
        return {"question": question, "answer": "stubbed-sql-answer"}

    monkeypatch.setattr(main_module, "run_txt_sql_query", fake_run_txt_sql_query)

    resp = client.post("/text-sql", data={"question": "How many customers?", "session_id": "s1"})
    assert resp.status_code == 200
    assert resp.json()["answer"] == "stubbed-sql-answer"


def test_report(monkeypatch):
    def fake_run_agents(question: str):
        return {"question": question, "answer": "stubbed-report"}

    monkeypatch.setattr(main_module, "run_agents", fake_run_agents)

    resp = client.post("/report", data={"question": "Generate a report"})
    assert resp.status_code == 200
    assert resp.json()["answer"] == "stubbed-report"

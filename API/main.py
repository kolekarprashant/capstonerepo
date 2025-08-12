from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile,Form
from services.image_process import run_extract_image
from services.rag_process import run_rag_query
from services.text_to_sql import run_txt_sql_query
from fastapi.middleware.cors import CORSMiddleware
from services.generate_report import run_agents
from logging_config import logger
load_dotenv()

app = FastAPI()
# for CORS issue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
memory_store = {}
@app.post("/extract-image")
async def rag_image(file: UploadFile = File(...),question: str = Form(...)):
    logger.info(f"Extracting image data for question: {question}")
    return await run_extract_image(file,question)

@app.post("/rag-pdf")
def rag_pdf(question: str = Form(...)):
    logger.info(f"Running RAG query for question: {question}")
    return run_rag_query(question)

@app.post("/text-sql")
def rag_text_sql(question: str = Form(...),session_id: str = Form(None)):
    logger.info(f"Running Text-to-SQL for session_id={session_id}, question: {question}")
    return run_txt_sql_query(session_id,memory_store,question)

@app.post("/report")
def report(question: str = Form(...)):
    logger.info(f"Generating report for question: {question}")
    return run_agents(question)
    
    

if __name__ == "__main__":
    app.run(debug=True)
   
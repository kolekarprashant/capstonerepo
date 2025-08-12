import os
from dotenv import load_dotenv
import boto3
from langchain_openai import AzureChatOpenAI
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from cohere_embedding import CohereEmbedding
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from fastapi import FastAPI, UploadFile
from tempfile import NamedTemporaryFile
from pathlib import Path
from logging_config import logger
load_dotenv()

app = FastAPI()

VECTOR_CACHE = {}

def extract_text_from_image_aws_textract(file_path):
    logger.info(f"Extracting text from image using AWS Textract: {file_path}")
    try:
        textract = boto3.client(
        'textract',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("AWS_TEXTTRACT_KEY"),
        aws_secret_access_key=os.getenv("AWS_TEXTTRACT_SECRET_ACCESS_KEY"))

        with open(file_path, 'rb') as document: 
            image_bytes = document.read()

        response = textract.detect_document_text(Document={'Bytes': image_bytes})
        lines = [item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"]
        full_text = "\n".join(lines)
        logger.info(f"Extracted {len(lines)} lines of text from image.")
        return full_text
    except Exception as e:
     logger.exception(f"Error during AWS Textract OCR: {e}")
    raise

async def run_extract_image(file: UploadFile, question: str):
    """
    extract text from upload image and create vector and pass to llm
    """
    logger.info(f"Received image file: {file.filename}")
    tmp_path: str =""
    
    if file.filename in VECTOR_CACHE:
        logger.info("Using cached vector store for this file.")
        vectorstore = VECTOR_CACHE[file]
    else:
        ext = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        logger.info(f"Temporary file saved at: {tmp_path}")

    ocr_text = extract_text_from_image_aws_textract(tmp_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(ocr_text)
    embedding_model = CohereEmbedding()
    vectorstore = FAISS.from_texts(chunks, embedding_model)

    llm = get_llm()
    memory = get_memory()
    retriever = create_retriever(vectorstore, llm, memory)
    logger.info(f"Querying LLM with question: {question}")
    response = retriever.invoke(question)
    print("Response:\n", response)
    answer = response.get("answer", "No answer returned")
    logger.info(f"Answer generated: {answer}")

    return {
        "question": question,
        "answer": answer
    }

def create_retriever(vectorstore, llm, memory):
   return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
  

def get_memory():
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    return memory

def get_llm():
    AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
    AZURE_API_KEY = os.getenv("AZURE_API_KEY")
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

    llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    api_key=AZURE_API_KEY,
    api_version="2024-12-01-preview",
    azure_endpoint=AZURE_ENDPOINT,
    openai_api_type="azure"
    )
    
    return llm
    
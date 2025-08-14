import os
from dotenv import load_dotenv
import boto3
import json
from langchain_openai import AzureChatOpenAI
from langchain_cohere import CohereEmbeddings
from langchain.schema.document import Document
import faiss
from langchain.vectorstores import FAISS
import numpy as np
from langchain.memory import ConversationBufferMemory
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.chains import ConversationalRetrievalChain
from logging_config import logger
load_dotenv()

s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION"))
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

def load_vectors_from_s3():
    bucket = os.getenv("S3_VECTOR_BUCKET_NAME")
    key = os.getenv("S3_VECTOR_FOLDER") + "customer_sales_vectors.json"
    logger.info(f"Loading vectors from S3 bucket '{bucket}', key '{key}'")
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read().decode("utf-8")
    vector_data = json.loads(content)
    return vector_data

def build_faiss_from_vectors(vector_data):
    logger.info("Building FAISS index from loaded vectors.")
    docs = []
    embeddings = []

    for item in vector_data:
        text = item.get("text", "")
        metadata = item.get("metadata", {})
        vector = item["vector"]
        docs.append(Document(page_content=text, metadata=metadata))
        embeddings.append(vector)
        
    logger.info(f"Total documents: {len(docs)}")
    try:
    # Convert embeddings to numpy array
        embedding_matrix = np.array(embeddings).astype(np.float32)
        embedding_function = CohereEmbeddings(
            model="embed-english-v3.0" 
        )

        # Build the FAISS index
        dim = embedding_matrix.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embedding_matrix)

        # Build docstore and ID map
        index_to_docstore_id = {i: str(i) for i in range(len(docs))}
        docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(docs)})

        # Now create the FAISS vectorstore
        vectorstore = FAISS(
            embedding_function,
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id,
            )
        logger.info(f"FAISS index built successfully with {len(docs)} documents.")
        return vectorstore
    except Exception as e:
            logger.exception(f"Error building FAISS index: {e}")
            raise

def run_rag_query(question:str):
    logger.info(f"Running RAG query: '{question}'")
    try:
        load_dotenv()
        vector_data = load_vectors_from_s3()
        vec_store = build_faiss_from_vectors(vector_data)
        retriever = vec_store.as_retriever()
        
        llm = get_llm()
        qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=False
        )
        response = qa.invoke(question)
        print("Chat History Debug:")
        for m in memory.chat_memory.messages:
            print(f"{m.type}: {m.content}")

        print("Response:\n", response)
        answer = response.get("answer", "No answer returned")
        return {
            "question": question,
            "answer": answer
        }
    except Exception as e:
        logger.exception(f"Error during RAG query execution: {e}")
        raise

def get_llm():
    llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    api_key=AZURE_API_KEY,
    api_version="2024-12-01-preview",
    azure_endpoint=AZURE_ENDPOINT,
    openai_api_type="azure"
    )
    return llm

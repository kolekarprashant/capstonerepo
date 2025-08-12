import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid
from dotenv import load_dotenv
import cohere
import boto3
import json
load_dotenv() 

cohere_api_key = os.getenv("COHERE_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION= os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("S3_VECTOR_BUCKET_NAME")

s3_client = boto3.client(
"s3", 
aws_access_key_id=AWS_ACCESS_KEY_ID,
aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
region_name=AWS_REGION)
co = cohere.Client(cohere_api_key)

def upload_json_to_s3(data: list, key: str):
    bucket = BUCKET_NAME
    json_bytes = json.dumps(data).encode("utf-8")
    s3_client.put_object(Bucket=bucket, Key=key, Body=json_bytes)
    print(f"Uploaded vector data to s3://{bucket}/{key}")


def load_and_split_pdfs(pdf_dir: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_docs = []

    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_dir, filename))
            docs = loader.load()
            chunks = splitter.split_documents(docs)
            all_docs.extend(chunks)

    return all_docs

def generate_and_upload_embeddings():
    print("all env variable values")
    print(cohere_api_key)
    print(AWS_ACCESS_KEY_ID)
    print(AWS_SECRET_ACCESS_KEY)
    print(AWS_REGION)
    print(BUCKET_NAME)
    load_dotenv()
    pdf_folder = r"C:\personal\GenAI\GenAICapstoneProject\pdfiles"
    docs = load_and_split_pdfs(pdf_folder)
    texts = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]
    embedding_model = co.embed(
        texts=texts,
        model="embed-english-v3.0",  
        input_type="search_document"
    )
    vectors = embedding_model.embeddings
    formatted_data = []
    for i, (vec, meta) in enumerate(zip(vectors, metadatas)):
        formatted_data.append({
            "id": str(uuid.uuid4()),
            "vector": vec,
            "metadata": meta,
            "text": texts[i]
        })
      
    s3_key = "vectors/" + "customer_sales_vectors.json"
    upload_json_to_s3(formatted_data, s3_key)



if __name__ == "__main__":  
    generate_and_upload_embeddings()
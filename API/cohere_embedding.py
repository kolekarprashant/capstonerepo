from langchain.embeddings.base import Embeddings
import cohere
import os
from dotenv import load_dotenv
load_dotenv()

class CohereEmbedding(Embeddings):
    def __init__(self, model="embed-english-v3.0"):
        self.model = model
        self.client = cohere.Client(os.getenv("COHERE_API_KEY"))

    def embed_documents(self, texts):
        response = self.client.embed(texts=texts, model=self.model,input_type="search_document")
        return response.embeddings

    def embed_query(self, text):
        response = self.client.embed(texts=[text], model=self.model,input_type="search_document")
        return response.embeddings[0]
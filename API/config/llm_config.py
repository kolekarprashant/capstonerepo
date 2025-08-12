import os
from dotenv import load_dotenv

load_dotenv()

azure_openai_llm_config = {
    "config_list": [
        {
            "model": os.getenv("AZURE_DEPLOYMENT_NAME"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "base_url": os.getenv("AZURE_ENDPOINT"),
            "api_type": "azure",
            "api_version": "2024-12-01-preview"
        }
    ],
    "temperature": 1,
    "timeout": 60
}
# import os
# from dotenv import load_dotenv

# load_dotenv()

# azure_openai_llm_config = {
#     "config_list": [
#         {
#             "model": os.getenv("AZURE_DEPLOYMENT_NAME"),
#             "api_key": os.getenv("AZURE_API_KEY"),
#             "base_url": os.getenv("AZURE_ENDPOINT"),
#             "api_type": "azure",
#             "api_version": "2024-12-01-preview"
#         }
#     ],
#     "temperature": 1,
#     "timeout": 60
# }

# from langchain_cohere import ChatCohere
# import os

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# # LangChain Cohere wrapper
# cohere_llm = ChatCohere(
#     cohere_api_key=COHERE_API_KEY,
#     model="command-r-plus",   
#     temperature=0.0,
# )

# # Adapter for AutoGen
# cohere_llm_config = {
#     "llm": cohere_llm,    
#     "name": "cohere-llm",
#     "cache": False
# }

import os

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

cohere_llm_config = {
    "config_list": [
        {
            "model": "command-r-plus",
            "api_key": os.getenv("COHERE_API_KEY"),
            "api_type": "cohere",
        }
    ],
    "temperature": 0.0,
    "timeout": 60,
}


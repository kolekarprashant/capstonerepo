# from agents.database_specialist import database_specialist
# from agents.chart_visualizer import chart_visualizer
# from agents.report_generator import report_generator
# from autogen import GroupChat, GroupChatManager, UserProxyAgent
#from config.llm_config import azure_openai_llm_config
#from config.llm_config import cohere_llm_config
from logging_config import logger
from langchain_cohere import ChatCohere
from agents.database_specialist import query_sqlite,db_schema
from agents.chart_visualizer import generate_chart
from agents.report_generator import generate_html_report
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.agents import create_tool_calling_agent, AgentExecutor
import json
import re


# user_proxy = UserProxyAgent(
#     name="User",
#     human_input_mode="NEVER",  
#     code_execution_config=False,
#     description="Initiates the flow and provides the query. Does not participate in data processing."
# )

# groupchat = GroupChat(
#     agents=[user_proxy, database_specialist, chart_visualizer,report_generator],
#     messages=[],
#     max_round=15
#     )

# manager = GroupChatManager(
#     groupchat=groupchat,
#     llm_config=cohere_llm_config,
# )
tools = [query_sqlite, generate_chart, generate_html_report]

llm = ChatCohere(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model="command-r-plus",
    temperature=0
)

schema_text = db_schema.replace("\n", " ")


prompt = ChatPromptTemplate.from_messages([
    ("system",
     f"You are a data assistant with access to the Northwind SQLite database.\n\n"
     f"Database Schema (must use exactly these names):\n{schema_text}\n\n"
     "⚠️ RULES:\n"
     "- Never invent or assume table/column names.\n"
     "- If unsure, check the schema above.\n\n"
     "Steps to follow:\n"
     "1. Ask the DatabaseSpecialist to write and run the SQL query to get the required data.\n"
     "2. Pass the CSV data to ChartVisualizer to generate the appropriate chart.\n"
     "   - The generated chart must have a timestamp in its filename (e.g., chart_YYYYMMDD_HHMMSS.png).\n"
     "   - Save the chart image to the configured S3 bucket.\n"
     "   - Use the public S3 URL of the chart in the HTML file.\n"
     "3. When calling generate_html_report, you MUST include:\n"
     "- overview (string)\n"
     "- query (string)\n"
     "- headers (list of strings)\n"
     "- rows (list of rows)\n"
     "- chart_url (string) → this must come from ChartVisualizer output\n"
     "4. Save the HTML report with a timestamp in its filename (e.g., report_YYYYMMDD_HHMMSS.html).\n"
     "5. Upload the HTML file to the configured S3 bucket.\n"
     "6. Return only the public S3 URL of the HTML file as JSON, in the format:\n\n"
     "{{\n"
     '  "html_url": "..."\n'
     "}}"),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

 
def run_agents(goal: str):
   result = agent_executor.invoke({"input": goal})
   output = result["output"]
   return get_file_url(output)
   

def get_file_url(output):
    match = re.search(r"\{.*\}", output, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            data = json.loads(json_str)
            return data.get("html_url")
        except json.JSONDecodeError:
            pass  

    return output
    

# def run_agents(goal: str):
#     logger.info(f"Starting run_agents with goal: {goal}")
#     message = f"""
# Generate a report based on the following goal:
# {goal}

# Steps to follow:
# 1. Ask the DatabaseSpecialist to write and run the SQL query to get the required data.
# 2. Pass the CSV data to ChartVisualizer to generate the appropriate chart. 
#    - The generated chart must have a timestamp in its filename (e.g., chart_YYYYMMDD_HHMMSS.png).
#    - Save the chart image to the configured S3 bucket.
#    - Use the public S3 URL of the chart in the html file.
# 3. Create a html report containing:
#    - Overview section (including the executed SQL query)
#    - Data table from the CSV
#    - Chart section showing the chart via its S3 URL
# 4. Save the html report with a timestamp in its filename (e.g., report_YYYYMMDD_HHMMSS.html).
# 5. Upload the html file to the configured S3 bucket.
# 6. Return only the public S3 URL of the html file as JSON so the Flask UI can display it as a clickable download link.
# """
#     try:
#             response = user_proxy.initiate_chat(
#                 manager,
#                 message=message
#             )
#             return response
#     except Exception as e:
#         logger.exception(f"Error during agents execution: {e}")
#         raise


# if __name__ == "__main__":
#     run_agents("Show me total sales of 5 product as bar graph.")
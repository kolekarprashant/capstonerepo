from agents.database_specialist import database_specialist
from agents.chart_visualizer import chart_visualizer
from agents.report_generator import report_generator
from autogen import GroupChat, GroupChatManager, UserProxyAgent
from config.llm_config import azure_openai_llm_config
from logging_config import logger

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  
    code_execution_config=False,
    description="Initiates the flow and provides the query. Does not participate in data processing."
)

groupchat = GroupChat(
    agents=[user_proxy, database_specialist, chart_visualizer,report_generator],
    messages=[],
    max_round=15
    )

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=azure_openai_llm_config,
)

def run_agents(goal: str):
    logger.info(f"Starting run_agents with goal: {goal}")
    message = f"""
Generate a report based on the following goal:
{goal}

Steps to follow:
1. Ask the DatabaseSpecialist to write and run the SQL query to get the required data.
2. Pass the CSV data to ChartVisualizer to generate the appropriate chart. 
   - The generated chart must have a timestamp in its filename (e.g., chart_YYYYMMDD_HHMMSS.png).
   - Save the chart image to the configured S3 bucket.
   - Use the public S3 URL of the chart in the html file.
3. Create a html report containing:
   - Overview section (including the executed SQL query)
   - Data table from the CSV
   - Chart section showing the chart via its S3 URL
4. Save the html report with a timestamp in its filename (e.g., report_YYYYMMDD_HHMMSS.html).
5. Upload the html file to the configured S3 bucket.
6. Return only the public S3 URL of the html file as JSON so the Flask UI can display it as a clickable download link.
"""
    try:
            response = user_proxy.initiate_chat(
                manager,
                message=message
            )
            return response
    except Exception as e:
        logger.exception(f"Error during agents execution: {e}")
        raise

def get_file_url(response):
    logger.debug("Extracting file URL from response...")
    for msg in response.chat_history:
        if msg.get("content", "").strip().endswith(".html"):
            return msg["content"].strip()
    logger.warning("No .html file URL found in response.")
    return None


# if __name__ == "__main__":
#     run_agents("Show me total sales of 5 product as bar graph.")
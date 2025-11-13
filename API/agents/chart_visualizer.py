from autogen import ConversableAgent, register_function
from config.llm_config import cohere_llm_config
#from config.llm_config import azure_openai_llm_config
#from tools.chart_utils import generate_chart
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import os
from datetime import datetime
import boto3
from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()

S3_BUCKET = os.getenv("S3_REPORT_BUCKET")
S3_REGION = os.getenv("AWS_REGION")
S3_BASE_URL = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com"

s3_client = boto3.client("s3", region_name=S3_REGION)


def upload_to_s3(local_path: str, s3_key: str) -> str:
    content_type = "text/html" if local_path.endswith(".html") else "image/png"
    s3_client.upload_file(local_path, S3_BUCKET, s3_key, ExtraArgs={"ContentType": content_type})
    return f"{S3_BASE_URL}/{s3_key}"


@tool(description="Generate a chart from CSV data and upload it to S3. Returns the public S3 URL of the chart.")
def generate_chart(csv_data: str, x: str, y: str, chart_type: str = "bar"):
    """
    Generate a chart from CSV data and upload it to S3.
    Returns the public S3 URL of the chart image.
    """
    os.makedirs("files", exist_ok=True)
    
    for file_name in os.listdir("files"):
        file_path = os.path.join("files", file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
    df = pd.read_csv(StringIO(csv_data))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chart_filename = f"output_chart_{timestamp}.png"
    chart_path = os.path.join("files", chart_filename)
    
    plt.figure(figsize=(10, 5))
    if chart_type == "bar":
        plt.bar(df[x], df[y])
    elif chart_type == "line":
        plt.plot(df[x], df[y])
    elif chart_type == "pie":
        df.set_index(x)[y].plot.pie(autopct='%1.1f%%')
    else:
        raise ValueError("Unsupported chart type.")
    
    plt.title(f"{chart_type.capitalize()} Chart of {y} vs {x}")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(chart_path)
    
    s3_key = f"reports/{chart_filename}"
    chart_url = upload_to_s3(chart_path, s3_key)
    
    return chart_url

# chart_visualizer = ConversableAgent(
#     name="ChartVisualizer",
#     system_message="You are a chart visualizer. Given CSV data, generate a chart using Python.",
#     llm_config=cohere_llm_config,
#     human_input_mode="NEVER",
# )

# register_function(
#     generate_chart,
#     caller=chart_visualizer,
#     executor=chart_visualizer,
#     description="Generates a chart (bar, line, or pie) from CSV data."
# )

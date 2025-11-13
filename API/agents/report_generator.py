from autogen import ConversableAgent,register_function
from config.llm_config import cohere_llm_config
#from config.llm_config import azure_openai_llm_config
import os
from datetime import datetime
import boto3
from langchain_core.tools import tool

S3_BUCKET = os.getenv("S3_REPORT_BUCKET")
S3_REGION = os.getenv("AWS_REGION")
S3_BASE_URL = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com"

s3_client = boto3.client("s3", region_name=S3_REGION)

def upload_to_s3(local_path: str, s3_key: str) -> str:
    content_type = "text/html" if local_path.endswith(".html") else "image/png"
    s3_client.upload_file(local_path, S3_BUCKET, s3_key, ExtraArgs={"ContentType": content_type})
    return f"{S3_BASE_URL}/{s3_key}"

@tool(description="Generate an HTML report with overview, SQL query, table, and chart. Returns S3 URL of the report.")
def generate_html_report(overview: str, query: str, headers: list[str], rows: list[tuple], chart_url: str) -> str:
    """
    Generates an HTML report with an overview, SQL query, data table, and chart.

    Args:
        overview (str): Short summary of the report.
        query (str): SQL query used to generate the data.
        headers (list[str]): Column headers.
        rows (list[tuple]): Query results.
        chart_url (str): Public URL to the chart image.

    Returns:
        str: Complete HTML content as a string.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("files", exist_ok=True)
    report_filename = f"report_{timestamp}.html"
    report_path = os.path.join("files", report_filename)
    print(f"char url: {chart_url}")

    # Build table rows
    table_html = "".join(
        f"<tr>{''.join(f'<td>{cell}</td>' for cell in row)}</tr>"
        for row in rows
    )

    # Build HTML
    html_content = f"""
    <html>
    <head>
        <title>Sales Report - {datetime.now().strftime('%Y-%m-%d')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            img {{ max-width: 100%; height: auto; margin-top: 20px; }}
            h1, h2 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h1>Report Summary</h1>
        <h2>Overview</h2>
        <p>{overview}</p>

        <h2>SQL Query</h2>
        <pre>{query}</pre>

        <h2>Data Table</h2>
        <table>
            <thead>
                <tr>{''.join(f'<th>{h}</th>' for h in headers)}</tr>
            </thead>
            <tbody>
                {table_html}
            </tbody>
        </table>

        <h2>Chart</h2>
        <img src="{chart_url}" alt="Sales Chart" />
    </body>
    </html>
    """
    with open(report_path, "w") as f:
        f.write(html_content)
        
    s3_key = f"reports/{report_filename}"
    report_url = upload_to_s3(report_path, s3_key)

    return report_url

# report_generator = ConversableAgent(
#     name="ReportGenerator",
#     system_message="""
# You are a report generation assistant. Your job is to:
# 1. Ask the database agent for CSV data based on a goal.
# 2. Capture and include the SQL query used for that data.
# 3. Ask the chart visualizer to generate a chart from the CSV.
# 4. Combine the following into a html report:
#     - Overview section (include the SQL query used)
#     - Data Table section
#     - Chart section
# 5. Save the html report with a timestamp in its name.

# Instructions:
# - Make sure the overview explains what the report shows and includes the actual SQL query executed.
# - Format all sections clearly using HTML with proper headings, tables, and styling for readability.
# """,
#     llm_config=cohere_llm_config,
#     human_input_mode="TERMINATE"
# )

# register_function(
#     generate_html_report,
#     caller=report_generator,
#     executor=report_generator,
#     description="Generates and saves a html report with summary, table, and chart. Accepts summary text, CSV data, and chart file path using a timestamp in the filename."
# )

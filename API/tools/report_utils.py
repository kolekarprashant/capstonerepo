import base64

def save_markdown_report(summary: str, csv_data: str, chart_path: str) -> str:
    rows = csv_data.strip().split("\n")
    headers = rows[0].split(",")
    data_rows = rows[1:]
    table_md = "| " + " | ".join(headers) + " |\n"
    table_md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for row in data_rows:
        table_md += "| " + " | ".join(row.split(",")) + " |\n"

    with open(chart_path, "rb") as f:
        chart_base64 = base64.b64encode(f.read()).decode()

    # Build Markdown report
    md_content = f"""# Report Summary

## Overview
{summary}

## Data Table
{table_md}

## Chart

![Chart](data:image/png;base64,{chart_base64})
"""

    # Save to file
    with open("report.md", "w") as f:
        f.write(md_content)

    return "Markdown report saved as `report.md`."


import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

def generate_chart(csv_data: str, x: str, y: str, chart_type: str = "bar"):
    df = pd.read_csv(StringIO(csv_data))
    
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
    plt.savefig("output_chart.png")
    return "Chart saved as output_chart.png"

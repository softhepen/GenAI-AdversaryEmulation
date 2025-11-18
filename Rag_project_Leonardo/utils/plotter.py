import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger()

# Load precision values from JSON reports located in subfolders
def load_precisions_from_output(base_dir='./output', report_filename='tool_precision_report.json'):
    labels = []       # Subfolder names used as labels
    precisions = []   # Corresponding precision values extracted from JSON

    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)
        if os.path.isdir(subfolder_path):
            json_path = os.path.join(subfolder_path, report_filename)
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                        precision = data.get('precision', None)
                        if precision is not None:
                            labels.append(subfolder)
                            precisions.append(precision)
                except Exception as e:
                    logger.info(f"Error reading {json_path}: {e}")
    
    return labels, precisions

# Plot a bar chart of precision values per subfolder
def plot_precisions(labels, precisions, title='Tool Name Precision', save_path='./results/precision_chart.png'):
    plt.figure(figsize=(12, 6))
    plt.bar(labels, precisions, color='cornflowerblue')
    plt.xlabel('Subfolder')
    plt.ylabel('Precision')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 1)  # Precision is normalized between 0 and 1
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.savefig(save_path)

# Plot a summary chart from a consolidated metric CSV (chrF, edit distance)
def plot_metric_summary(
    csv_path,
    chart_path,
    metric_name='score',         # Display name of the metric
    score_column='score',        # Column containing the metric values
    score_range=(0, 1),          # Range of values for the x-axis (edit-distance: 0–1, chrF: 0–100)
    decimal=','                  # Decimal separator used in the CSV
):
    df = pd.read_csv(csv_path, decimal=decimal)

    required_cols = {'report', 'file', score_column}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    # Create label by combining report name and filename 
    df['label'] = df.apply(
        lambda row: f"{row['report']}_{row['file'].replace('.txt', '')}", axis=1
    )

    df_sorted = df.sort_values(by=score_column, ascending=False)

    fig, ax = plt.subplots(figsize=(16, max(6, len(df_sorted) * 0.5)), constrained_layout=True)
    ax.barh(df_sorted['label'], df_sorted[score_column], color='cornflowerblue')
    ax.set_xlabel(f'{metric_name} ({score_range[1]})')
    ax.set_ylabel('report_file')
    ax.set_title(f'{metric_name}')
    ax.set_xlim(score_range)
    ax.set_xticks([
        round(score_range[0] + i * (score_range[1] - score_range[0]) / 5, 2)
        for i in range(6)
    ])
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    ax.tick_params(axis='y', labelsize=8)

    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    fig.savefig(chart_path)
    plt.close(fig)

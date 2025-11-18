import os
import pandas as pd
from pathlib import Path
from utils.utils import finalize_log
from utils.similaritychrf import match_chrf, extract_max_score_chrf
from utils.similarityeditdistance import match_edit_distance, extract_max_score_edit
from utils.plotter import (
    load_precisions_from_output,
    plot_precisions,
    plot_metric_summary
)

def update_match_found(csv_path, score_column, threshold, separator=",", decimal="."):
    # Load CSV with locale-aware decimal handling
    df = pd.read_csv(csv_path, sep=separator, decimal=decimal)

    # Normalize score column to float
    df[score_column] = df[score_column].astype(str).str.replace(",", ".").astype(float)

    # Update match_found based on threshold
    df["match_found"] = df[score_column] >= threshold

    # Determine metric name from score column
    metric_name = score_column.replace("_score", "").replace("bleu", "bleu").replace("chrf", "chrf").replace("edit", "editdistance")

    # Prepare output path
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_name = f"{base_name}_{threshold}.csv"
    output_folder = os.path.join("results", metric_name)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_name)

    # Save updated CSV
    df.to_csv(output_path, index=False)

    return df



def run_evaluation_pipeline(report_name, group, report_folder, commands_folder, logger):
    # Run matching
    match_chrf(commands_folder, "input/ground_truth/tools_ground_truth.csv", export_csv=True, output_dir=report_folder)
    match_edit_distance(commands_folder, "input/ground_truth/tools_ground_truth.csv", export_csv=True, output_dir=report_folder)

    # Finalize log
    finalize_log(logger, log_dir="logs", reportname=report_name, group=group)

    # Create results folder
    os.makedirs("results", exist_ok=True)

    # Plot precision and similarity charts
    labels, precisions = load_precisions_from_output('./output')
    plot_precisions(labels, precisions)

    # Extract max scores
    extract_max_score_chrf(base_dir='./output', target_filename='match_results_chrf.csv', output_csv='results/chrf/chrf_summary.csv')
    extract_max_score_edit(base_dir='./output', target_filename='match_results_edit_distance.csv', output_csv='results/editdistance/edit_summary.csv')

    # Check if any .csv file exists in results/
    results_path = Path("results")

    # Search for summary CSVs inside subfolders
    summary_files = {
        "chrf": next(results_path.glob("chrf/*summary.csv"), None),
        "editdistance": next(results_path.glob("editdistance/*summary.csv"), None)
    }

    # Proceed only if all expected files are found
    if all(summary_files.values()):
    # Plot metric summaries
        plot_metric_summary(
            csv_path=summary_files["chrf"],
            chart_path=results_path / "chrf" / "chrf_summary_plot.png",
            metric_name="chrF",
            score_column="chrf_score",
            score_range=(0, 100)
        )

        plot_metric_summary(
            csv_path=summary_files["editdistance"],
            chart_path=results_path / "editdistance" / "edit_summary_plot.png",
            metric_name="Edit Distance",
            score_column="edit_score",
            score_range=(0, 1)
        )

        # Apply thresholds and save updated match_found
        update_match_found(str(summary_files["chrf"]), "chrf_score", threshold=20.0)
        update_match_found(str(summary_files["editdistance"]), "edit_score", threshold=0.3)
    else:
        logger.warning("No summary .csv files found in 'results/'. Skipping plotting and evaluation.")

from pathlib import Path

import pandas as pd

from .loader import clean_data  # Reuse our cleaning function


def process_file(raw_filepath: Path, processed_dir: Path):
    """
    Processes a single CSV file:
      - Reads the CSV file from raw_filepath.
      - Cleans it using clean_data().
      - Adds a course identifier based on the filename.
      - Saves the cleaned data to processed_dir, appending '_cleaned' to the filename.
    """
    # Read the CSV directly from the provided raw_filepath.
    df = pd.read_csv(raw_filepath)

    # Clean the data using our cleaning function.
    df_cleaned = clean_data(df)

    # Derive a course name from the filename.
    # We'll replace underscores with spaces and then apply title-case.
    # For files ending with '_data', we want a special rule.
    raw_stem = raw_filepath.stem
    if raw_stem.lower() == "dummy_data":
        course_name = "Dummy Data"
    elif raw_stem.endswith("_data"):
        # Remove the trailing '_data' and then replace underscores with spaces.
        course_name = raw_stem.replace("_data", "").replace("_", " ").title()
    else:
        course_name = raw_stem.replace("_", " ").title()

    if "course" not in df_cleaned.columns:
        df_cleaned["course"] = course_name

    # Define the output file path in the processed directory.
    processed_filepath = processed_dir / f"{raw_filepath.stem}_cleaned.csv"
    df_cleaned.to_csv(processed_filepath, index=False)
    print(f"Processed file saved to {processed_filepath}")


def process_all_files(raw_dir: Path = None, processed_dir: Path = None):
    """
    Processes all CSV files in raw_dir and saves the cleaned versions to processed_dir.
    If raw_dir or processed_dir are not provided, they default to:
      raw_dir: <project_root>/data/raw
      processed_dir: <project_root>/data/processed
    """
    # Determine project root if directories are not provided.
    if raw_dir is None or processed_dir is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        if raw_dir is None:
            raw_dir = project_root / "data" / "raw"
        if processed_dir is None:
            processed_dir = project_root / "data" / "processed"

    # Ensure processed_dir exists.
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Find all CSV files in the raw directory.
    csv_files = list(raw_dir.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {raw_dir}")
        return

    for csv_file in csv_files:
        print(f"Processing {csv_file.name}...")
        process_file(csv_file, processed_dir)


if __name__ == "__main__":
    process_all_files()

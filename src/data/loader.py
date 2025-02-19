import os
from pathlib import Path

import pandas as pd


def load_csv_data(filename: str) -> pd.DataFrame:
    """
    Loads a CSV file from the data/raw directory at the project root.

    Parameters:
        filename (str): The name of the CSV file (e.g., "course_data.csv")

    Returns:
        pd.DataFrame: The loaded data.
    """
    # Compute the project root (assuming this file is in project/src/data/)
    project_root = Path(__file__).resolve().parent.parent.parent
    file_path = project_root / "data" / "raw" / filename

    # Read the CSV file. Adjust the delimiter if necessary.
    df = pd.read_csv(file_path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and preprocesses the data for analysis.

    - Converts any column whose name contains "%" to a numeric type.
    - Fills missing numeric values in percentage columns with 0.
    - Fills missing response columns (like 'failed3_response') with empty strings.

    Parameters:
        df (pd.DataFrame): The raw data.

    Returns:
        pd.DataFrame: The cleaned data.
    """
    # Identify columns with "%" in the name (e.g., %failed, %giveup, %trigger_goto, %failed1, etc.)
    percent_cols = [col for col in df.columns if "%" in col]
    for col in percent_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Identify columns that contain responses. Adjust the list if you have more columns.
    response_cols = [col for col in df.columns if "response" in col.lower()]
    for col in response_cols:
        df[col] = df[col].fillna("")

    return df


if __name__ == "__main__":
    filename = "prealgebra_2_data.csv"
    df = load_csv_data(filename)
    df = clean_data(df)

    # Save cleaned data to data/processed directory
    processed_filepath = os.path.join("data", "processed", "cleaned_data.csv")
    df.to_csv(processed_filepath, index=False)

    print(f"Cleaned data saved to {processed_filepath}")

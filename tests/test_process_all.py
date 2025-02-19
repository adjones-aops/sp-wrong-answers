from pathlib import Path

import pandas as pd

from src.data.process_all import process_file


def create_dummy_csv(path: Path):
    data = {
        "document_name": ["Dummy Course"],
        "pointer": ["dummy1"],
        "num_responses": [100],
        "%failed1": [20],
        "failed1_response": ["[0]"],
        "%failed2": [10],
        "failed2_response": ["[1]"],
        "%failed3": [5],
        "failed3_response": ["[2]"],
        "%failed": [35],
        "%giveup": [0],
        "%trigger_goto": [0],
    }
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)


def test_process_file(tmp_path):
    # Create temporary raw and processed directories
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir()

    # Create a dummy CSV file in raw_dir
    dummy_csv = raw_dir / "dummy_data.csv"
    create_dummy_csv(dummy_csv)

    # Call process_file with the dummy CSV and the temporary processed directory
    process_file(dummy_csv, processed_dir)

    # Check that the processed file exists
    processed_file = processed_dir / "dummy_data_cleaned.csv"
    assert processed_file.exists(), "Processed file was not created"

    # Optionally, load the processed file and check for the 'course' column
    df_processed = pd.read_csv(processed_file)
    assert "course" in df_processed.columns
    # Check that the course name is computed as expected (e.g., "Dummy Data")
    expected_course = "Dummy Data".title()
    assert df_processed["course"].iloc[0] == expected_course

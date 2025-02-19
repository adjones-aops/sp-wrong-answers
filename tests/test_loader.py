import pandas as pd
import pytest

from src.data.loader import clean_data


@pytest.fixture
def sample_raw_data():
    # Create a sample dataframe similar to your CSV data
    data = {
        "document_id": [10299, 10299],
        "document_name": ["What is a Percent?", "What is a Percent?"],
        "version": [22, 22],
        "pointer": ["body11MultiAnswerProblem", "body13MultiAnswerProblem"],
        "num_responses": [7592, 8072],
        "%failed": [4, 8],
        "%giveup": [0, 0],
        "%trigger_goto": [0, 0],
        "%failed1": [3.0, 8.0],
        "failed1_response": ["[1]", "[0]"],
        "%failed2": [1.0, 0.0],
        "failed2_response": ["[2]", "[2]"],
        "%failed3": [None, None],
        "failed3_response": [None, None],
    }
    return pd.DataFrame(data)


def test_clean_data(sample_raw_data):
    # Clean the sample data
    cleaned_df = clean_data(sample_raw_data.copy())

    # Check that percentage columns are converted to numeric and NaN filled with 0
    assert cleaned_df["%failed3"].dtype.kind in "fc"  # float or complex type
    # NaNs in %failed3 should be replaced with 0.0
    assert (cleaned_df["%failed3"] == 0).all()

    # Check that response columns have no NaN values (they should be replaced with empty strings)
    assert cleaned_df["failed3_response"].isna().sum() == 0
    # And check that any NaN was replaced with an empty string
    assert (cleaned_df["failed3_response"] == "").all()

    # Optionally, you can check that existing values remain unchanged
    # For example, for the first row
    row0 = cleaned_df.iloc[0]
    assert row0["%failed"] == 4
    assert row0["failed1_response"] == "[1]"
    assert row0["%failed2"] == 1.0
    assert row0["failed2_response"] == "[2]"

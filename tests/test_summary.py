import pandas as pd

from src.analysis.summarize import build_summary_table, summarize_wrong_answers


def test_summarize_wrong_answers():
    # Create a sample row as a Series
    row = pd.Series(
        {
            "%failed1": 30,
            "failed1_response": "[0]",
            "%failed2": 15,
            "failed2_response": "[1]",
            "%failed3": 5,
            "failed3_response": "[2]",
        }
    )
    summary = summarize_wrong_answers(row)
    expected = "1) [0] (30%), 2) [1] (15%), 3) [2] (5%)"
    assert summary == expected


def test_build_summary_table():
    # Create a sample DataFrame with a few rows.
    data = {
        "document_name": ["Course A", "Course A"],
        "pointer": ["p1", "p2"],
        "num_responses": [100, 200],
        "%failed1": [20, 30],
        "failed1_response": ["[0]", "[1]"],
        "%failed2": [10, 15],
        "failed2_response": ["[2]", "[3]"],
        "%failed3": [5, 10],
        "failed3_response": ["[4]", "[5]"],
        # Include extra columns too.
        "%failed": [35, 55],
        "%giveup": [0, 0],
        "%trigger_goto": [0, 0],
    }
    df = pd.DataFrame(data)
    summary_table = build_summary_table(df)
    # Check that summary_table has the desired columns.
    for col in [
        "document_name",
        "pointer",
        "num_responses",
        "%failed",
        "%giveup",
        "%trigger_goto",
        "%wrong_combined",
        "top three wrong answers",
    ]:
        assert col in summary_table.columns
    # Verify that %wrong_combined is computed correctly (20+10+5 and 30+15+10)
    expected_wrong_combined = [35, 55]
    pd.testing.assert_series_equal(
        summary_table["%wrong_combined"], pd.Series(expected_wrong_combined, name="%wrong_combined")
    )

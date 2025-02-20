import pandas as pd


def summarize_wrong_answers(row):
    """
    Returns a string summarizing the top three wrong answers.
    For example: '1) [0,1] (30%), 2) [0,1,2,3] (15%), 3) [0,1,5,6] (5%)'
    """
    items = []
    for i in [1, 2, 3]:
        pct = row.get(f"%failed{i}", 0)
        resp = row.get(f"failed{i}_response", "")
        if pd.notna(pct) and pct > 0:
            items.append(f"{i}) {resp} ({pct}%)")
    return ", ".join(items)


def filter_data(df: pd.DataFrame, min_attempts: int) -> pd.DataFrame:
    """
    Filters data based on a minimum number of responses and removes bogus rows.
    Computes a combined wrong percentage and filters out rows where it is 99% or higher.
    """
    # Ensure we work on a copy to avoid SettingWithCopyWarning.
    df = df.copy()

    if "num_responses" in df.columns:
        df = df[df["num_responses"] >= min_attempts]

    # Use .loc to explicitly assign to a new column.
    df.loc[:, "%wrong_combined"] = df["%failed1"].fillna(0) + df["%failed2"].fillna(0) + df["%failed3"].fillna(0)

    # Filter out rows where the combined wrong percentage is 99% or higher.
    df = df[df["%wrong_combined"] < 99]

    df = df[df["%failed"] < 100]
    return df


def build_column_toggles(df: pd.DataFrame, sidebar) -> list[str]:
    """
    Returns the list of columns to display based on individual toggle checkboxes.
    Always includes 'document_name', 'pointer', 'num_responses', 'top three wrong answers'.
    """
    base_cols = ["document_name", "pointer", "num_responses", "top three wrong answers"]
    optional_cols = []

    if "%failed" in df.columns:
        if sidebar.checkbox("Show %failed", value=False):
            optional_cols.append("%failed")
    if "%giveup" in df.columns:
        if sidebar.checkbox("Show %giveup", value=False):
            optional_cols.append("%giveup")
    if "%trigger_goto" in df.columns:
        if sidebar.checkbox("Show %trigger_goto", value=False):
            optional_cols.append("%trigger_goto")
    if "%wrong_combined" in df.columns:
        if sidebar.checkbox("Show %wrong_combined", value=False):
            optional_cols.append("%wrong_combined")

    return base_cols + optional_cols

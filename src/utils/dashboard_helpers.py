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
    Filters data based on a minimum number of responses.
    Also computes %wrong_combined if not present, then filters out bogus rows.
    """
    if "num_responses" in df.columns:
        df = df[df["num_responses"] >= min_attempts]
    if "%wrong_combined" not in df.columns:
        df["%wrong_combined"] = df["%failed1"].fillna(0) + df["%failed2"].fillna(0) + df["%failed3"].fillna(0)
    # Remove rows where %wrong_combined is 99% or more (probably bogus)
    df = df[df["%wrong_combined"] < 99]
    # Remove rows where %failed is 100% (probably bogus)
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

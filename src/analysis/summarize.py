import pandas as pd


def summarize_wrong_answers(row):
    """
    Creates a single string summarizing the top three wrong answers, e.g.:
    '1) [0,1] (3%), 2) [0,1,2,3] (3%), 3) [0,1,5,6] (2%)'
    Uses the individual %failed1, %failed2, %failed3 values.
    """
    items = []
    for i in [1, 2, 3]:
        wrong_pct = row.get(f"%failed{i}", 0)
        wrong_resp = row.get(f"failed{i}_response", "")
        if pd.notna(wrong_pct) and wrong_pct > 0:
            items.append(f"{i}) {wrong_resp} ({wrong_pct}%)")
    return ", ".join(items)


def build_summary_table(df):
    """
    Builds a summary table that retains:
      - document_name
      - pointer
      - num_responses
      - %failed, %giveup, %trigger_goto (if present)
      - %failed1, failed1_response, %failed2, failed2_response, %failed3, failed3_response (if present)
      - %wrong_combined (the sum of %failed1, %failed2, %failed3)
      - top three wrong answers (a single string)
    """
    df_copy = df.copy()

    # If %wrong_combined isn't already computed, compute it
    if "%wrong_combined" not in df_copy.columns:
        df_copy["%wrong_combined"] = (
            df_copy["%failed1"].fillna(0) + df_copy["%failed2"].fillna(0) + df_copy["%failed3"].fillna(0)
        )

    # Create the 'top three wrong answers' column
    df_copy["top three wrong answers"] = df_copy.apply(summarize_wrong_answers, axis=1)

    # Define the columns we want to keep (if they exist in df)
    desired_cols = [
        "document_name",
        "pointer",
        "num_responses",
        "%failed",
        "%giveup",
        "%trigger_goto",
        "%failed1",
        "failed1_response",
        "%failed2",
        "failed2_response",
        "%failed3",
        "failed3_response",
        "%wrong_combined",
        "top three wrong answers",
    ]

    # Only select columns that actually exist in the DataFrame
    keep_cols = [col for col in desired_cols if col in df_copy.columns]

    # Return the subset with the columns we want to keep
    summary_table = df_copy[keep_cols]
    return summary_table


def filter_by_num_responses_percentile(df, percentile=0.25):
    """
    Filters out rows that fall below the given percentile of num_responses.
    E.g., percentile=0.25 -> remove bottom 25% of problems by response count.
    """
    cutoff = df["num_responses"].quantile(percentile)
    return df[df["num_responses"] >= cutoff]


if __name__ == "__main__":
    # 1. Load your cleaned CSV file from data/processed
    df = pd.read_csv("data/processed/cleaned_data.csv")

    # 2. Compute %wrong_combined if not already computed
    df["%wrong_combined"] = df["%failed1"].fillna(0) + df["%failed2"].fillna(0) + df["%failed3"].fillna(0)

    # 3. Filter out rows with zero %wrong_combined (optional) and those >= 99 (bogus)
    df = df[df["%wrong_combined"] > 0]
    df = df[df["%wrong_combined"] < 99]

    # 4. Filter out problems in the bottom 25% by num_responses (optional)
    df = filter_by_num_responses_percentile(df, percentile=0.25)

    # 5. Sort the remaining rows by %wrong_combined in descending order (optional)
    df = df.sort_values(by="%wrong_combined", ascending=False)

    # 6. Build the summary table
    summary_table = build_summary_table(df)

    # 7. Display in console
    print(summary_table.to_string(index=False))

    # 8. Export the entire table (no top-20 limit) to CSV
    summary_table.to_csv("all_failures_summary.csv", index=False)
    print("Exported summary to all_failures_summary.csv")

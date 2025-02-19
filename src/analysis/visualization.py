import os

import matplotlib.pyplot as plt
import pandas as pd


def load_cleaned_data():
    filepath = os.path.join("data", "processed", "cleaned_data.csv")
    return pd.read_csv(filepath)


def get_worst_problems(df, percentile=0.95):
    """
    Returns a DataFrame of only the worst problems, defined by the given percentile
    of %failed. E.g. percentile=0.90 -> top 10% of problems by %failed.
    """
    threshold = df["%failed"].quantile(percentile)
    return df[df["%failed"] >= threshold]


def process_failed_responses(df):
    """Explode the multiple responses into rows."""
    response_columns = ["failed1_response", "failed2_response", "failed3_response"]
    for col in response_columns:
        df[col] = df[col].astype(str).str.replace(r"[\[\]\"]", "", regex=True)
        df[col] = df[col].str.split(",")
        df = df.explode(col)
    return df


def group_rare_responses(df, top_n=10):
    """
    Replace responses outside the top_n most common with 'Other'.
    Assumes the exploded column is named 'failed_response' if we do a melt
    or we rename columns accordingly.
    """
    if "failed_response" not in df.columns:
        df = df.rename(columns={"failed1_response": "failed_response"})
    response_counts = df["failed_response"].value_counts()
    top_responses = response_counts.index[:top_n]
    df["failed_response"] = df["failed_response"].where(df["failed_response"].isin(top_responses), "Other")
    return df


def plot_stacked_bar_chart(df):
    """Creates a stacked bar chart of common failure responses per question."""

    # If we haven't melted yet, let's pivot on pointer + failed_response
    failure_counts = df.groupby(["pointer", "failed_response"]).size().unstack(fill_value=0)

    # Convert counts to percentages
    failure_percentages = failure_counts.div(failure_counts.sum(axis=1), axis=0) * 100

    # Escape dollar signs
    failure_percentages.columns = failure_percentages.columns.str.replace(r"\$", r"\\$", regex=True)

    # Plot
    ax = failure_percentages.plot(kind="bar", stacked=True, figsize=(16, 6), colormap="viridis")
    ax.set_ylabel("Percentage of Failures")
    ax.set_xlabel("Question (Pointer)")
    ax.set_title("Distribution of Failed Responses (Worst Problems Only)")
    ax.legend(title="Incorrect Response", bbox_to_anchor=(1.0, 1.0))

    plt.tight_layout()
    plt.show()


def main():
    df = load_cleaned_data()

    # 1) Filter to worst problems (top 10% by %failed)
    worst_df = get_worst_problems(df, percentile=0.90)

    # 2) Explode the failure responses
    worst_df = process_failed_responses(worst_df)

    # 3) Group rare responses
    worst_df = group_rare_responses(worst_df, top_n=10)

    # 4) Plot
    plot_stacked_bar_chart(worst_df)


if __name__ == "__main__":
    main()

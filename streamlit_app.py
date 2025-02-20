import pandas as pd
import streamlit as st

from src.analysis.visualization import show_bubble_chart
from src.utils.dashboard_helpers import build_column_toggles, filter_data, summarize_wrong_answers

# Define course files and URL prefixes.
COURSE_FILES = {
    "Prealgebra 1": "data/processed/prealgebra_1_data_cleaned.csv",
    "Prealgebra 2": "data/processed/prealgebra_2_data_cleaned.csv",
    "Algebra A": "data/processed/algebra_a_data_cleaned.csv",
}

COURSE_LINK_PREFIX = {
    "Prealgebra 1": "https://www.aops.com/crypt/composite/519/",
    "Prealgebra 2": "https://www.aops.com/crypt/composite/520/",
    "Algebra A": "https://www.aops.com/crypt/composite/518/",
}


def load_and_rename_data(course_file: str, course_key: str) -> pd.DataFrame:
    """
    Loads CSV, creates the 'top three wrong answers' column,
    and constructs a 'document_link' column that embeds the document_name
    in the URL as a query parameter for later extraction.
    """
    df = pd.read_csv(course_file)
    # Use helper function to summarize wrong answers.
    df["top three wrong answers"] = df.apply(summarize_wrong_answers, axis=1)

    prefix = COURSE_LINK_PREFIX.get(course_key, "")

    def make_link(row):
        if "document_id" in row and "document_name" in row:
            base_url = f"{prefix}{row['document_id']}"
            # Append document_name as a query parameter so we can extract it for display.
            return f"{base_url}?docName={row['document_name']}"
        return ""

    df["document_link"] = df.apply(make_link, axis=1)
    return df


def select_course() -> str:
    st.sidebar.header("Dashboard Filters")
    return st.sidebar.selectbox("Select Course", list(COURSE_FILES.keys()))


def main():
    st.set_page_config(layout="wide")
    st.title("Common Mistakes Dashboard")

    # 1) Select Course
    selected_course = select_course()
    course_file = COURSE_FILES[selected_course]

    # 2) Load data
    df = load_and_rename_data(course_file, selected_course)

    # 3) Filter data using the helper. This applies:
    #    - Minimum number of responses (via slider)
    #    - Computation of "%wrong_combined" and filtering out rows with 99%+.
    if "num_responses" in df.columns:
        max_responses = int(df["num_responses"].max())
    else:
        max_responses = 100

    min_attempts = st.sidebar.slider(
        "Minimum Number of Responses", min_value=0, max_value=max_responses, value=30, key="min_attempts"
    )
    df = filter_data(df, min_attempts)

    # 4) Build the list of columns to display using the helper.
    # The helper returns ["document_name", "pointer", "num_responses", "top three wrong answers"]
    # plus any optional columns the user toggles (e.g. "%failed", etc.)
    # We swap out "document_name" for "document_link" so that our clickable link is used.
    columns_to_display = build_column_toggles(df, st.sidebar)
    if "document_name" in columns_to_display:
        idx = columns_to_display.index("document_name")
        columns_to_display[idx] = "document_link"

    # 5) Build the Sort by dropdown.
    # Start with "Chronological" and optionally "num_responses"
    sort_options = ["Chronological"]
    if "num_responses" in df.columns:
        sort_options.append("num_responses")

    # Determine which optional columns were toggled.
    # (They will be among columns_to_display if activated.)
    optional_cols = [
        col
        for col in columns_to_display
        if col not in ["document_link", "pointer", "num_responses", "top three wrong answers"]
    ]

    # Add these to the sort options.
    sort_options.extend(optional_cols)

    sort_option = st.sidebar.selectbox("Sort by", options=sort_options, index=0)

    # Apply the chosen sort if not "Chronological".
    if sort_option != "Chronological" and sort_option in df.columns:
        df = df.sort_values(by=sort_option, ascending=False)

    # 6) Display the interactive data table.
    st.header(f"Summary for {selected_course}")
    if df.empty:
        st.warning("No data available after filtering. Please adjust your filters.")
    else:
        sub_df = df[columns_to_display].copy()

        st.data_editor(
            sub_df,
            column_config={
                "document_link": st.column_config.LinkColumn(
                    label="Document",
                    help="Click to view the document",
                    # This regex captures everything after '?docName=' for display.
                    display_text=r"\?docName=(.*)$",
                ),
            },
            hide_index=True,
        )

    # 7) Display visualizations.
    st.header("Visualizations")
    show_bubble_chart(df)


if __name__ == "__main__":
    main()

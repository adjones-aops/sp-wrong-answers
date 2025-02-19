import pandas as pd
import streamlit as st

from src.analysis.visualization import show_bubble_chart
from src.utils.dashboard_helpers import build_column_toggles  # returns the list of columns user wants to display
from src.utils.dashboard_helpers import filter_data  # filters out data with < min_attempts and bogus rows
from src.utils.dashboard_helpers import summarize_wrong_answers

COURSE_FILES = {
    "Prealgebra 1": "data/processed/prealgebra_1_data_cleaned.csv",
    "Prealgebra 2": "data/processed/prealgebra_2_data_cleaned.csv",
    "Algebra A": "data/processed/algebra_a_data_cleaned.csv",
}


def load_and_rename_data(course_file: str) -> pd.DataFrame:
    """
    Loads CSV and creates the 'top three wrong answers' column.
    """
    df = pd.read_csv(course_file)
    df["top three wrong answers"] = df.apply(summarize_wrong_answers, axis=1)
    return df


def select_course() -> str:
    st.sidebar.header("Dashboard Filters")
    selected = st.sidebar.selectbox("Select Course", list(COURSE_FILES.keys()))
    return selected


def main():
    st.set_page_config(layout="wide")
    st.title("Common Mistakes Dashboard")

    # 1) Select Course
    selected_course = select_course()
    course_file = COURSE_FILES[selected_course]

    # 2) Load data
    df = load_and_rename_data(course_file)

    # 3) Filter by minimum # of responses
    max_responses = int(df["num_responses"].max()) if "num_responses" in df.columns else 100
    min_attempts = st.sidebar.slider("Minimum Number of Responses", 0, max_responses, 30)
    df = filter_data(df, min_attempts)  # Also filters out rows with >=99% combined

    # 4) Column Toggles: user picks which columns to display
    #    (Assume build_column_toggles always includes 'top three wrong answers' and 'pointer' etc.)
    columns_to_display = build_column_toggles(df, st.sidebar)

    # 5) Build dynamic sort options
    #    Always show "Chronological" (no sort) and "num_responses"
    #    plus any columns that the user toggled on (and exist in df).
    sort_options = ["Chronological"]
    if "num_responses" in df.columns:
        sort_options.append("num_responses")

    # For each toggled column (besides 'pointer', 'top three wrong answers', etc.), if it's in the DataFrame,
    # add it to sort_options. We'll only add columns that are actually toggled on and exist in the DataFrame.
    # This ensures that user can only sort by columns that are visible.
    for col in columns_to_display:
        # Skip the always columns if you prefer not to sort by them
        # For example, you might skip 'pointer' or 'top three wrong answers'.
        if col not in ("pointer", "top three wrong answers", "num_responses", "document_name"):
            # add it if it's not already in sort_options
            if col not in sort_options and col in df.columns:
                sort_options.append(col)

    sort_option = st.sidebar.selectbox("Sort by", options=sort_options, index=0)

    # 6) Apply sorting if user picked something besides "Chronological"
    if sort_option != "Chronological" and sort_option in df.columns:
        df = df.sort_values(by=sort_option, ascending=False)

    # 7) Display results
    st.header(f"Summary for {selected_course}")
    if df.empty:
        st.warning("No data available after filtering. Please adjust your filters.")
    else:
        st.dataframe(df[columns_to_display])

    st.header("Visualizations")
    show_bubble_chart(df)


if __name__ == "__main__":
    main()

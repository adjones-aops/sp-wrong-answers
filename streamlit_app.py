import streamlit as st
import pandas as pd
from pathlib import Path
from src.utils.dashboard_helpers import summarize_wrong_answers, filter_data, build_column_toggles

# Course file mapping (with updated file names)
COURSE_FILES = {
    "Prealgebra 1": "data/processed/prealgebra_1_data_cleaned.csv",
    "Prealgebra 2": "data/processed/prealgebra_2_data_cleaned.csv",
    "Algebra A":     "data/processed/algebra_a_data_cleaned.csv",
}

def load_and_rename_data(course_file: str) -> pd.DataFrame:
    """
    Loads CSV and creates the 'top three wrong answers' column.
    """
    df = pd.read_csv(course_file)
    # Always create top three wrong answers
    df["top three wrong answers"] = df.apply(summarize_wrong_answers, axis=1)
    return df

def select_course() -> str:
    st.sidebar.header("Dashboard Filters")
    selected = st.sidebar.selectbox("Select Course", list(COURSE_FILES.keys()))
    return selected

def main():
    st.set_page_config(layout="wide")
    st.title("Common Mistakes Dashboard")
    
    # Course selection
    selected_course = select_course()
    course_file = COURSE_FILES[selected_course]
    
    # Load data
    df = load_and_rename_data(course_file)
    
    # Sidebar filter: Minimum responses
    max_responses = int(df["num_responses"].max()) if "num_responses" in df.columns else 100
    min_attempts = st.sidebar.slider("Minimum Number of Responses", 0, max_responses, 30)
    
    # Filter data
    df = filter_data(df, min_attempts)
    
    # Sidebar: Sorting option (if desired)
    sort_option = st.sidebar.selectbox("Sort by", options=["None", "num_responses", "%failed", "%wrong_combined"], index=0)
    if sort_option != "None" and sort_option in df.columns:
        df = df.sort_values(by=sort_option, ascending=False)
    
    # Build column toggles from our helper in dashboard_helpers
    columns_to_display = build_column_toggles(df, st.sidebar)
    
    st.header(f"Summary for {selected_course}")
    if df.empty:
        st.warning("No data available after filtering. Please adjust your filters.")
    else:
        st.dataframe(df[columns_to_display])
    
    st.header("Visualizations")
    st.write("Add interactive charts here that respond to the selected filters.")

if __name__ == "__main__":
    main()

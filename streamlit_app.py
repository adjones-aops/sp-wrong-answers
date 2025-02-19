import pandas as pd
import streamlit as st

from src.analysis.summarize import build_summary_table

# Define a mapping from course names to their cleaned data file paths
COURSE_FILES = {
    "Prealgebra 1": "data/processed/prealgebra_1_data_cleaned.csv",
    "Prealgebra 2": "data/processed/prealgebra_2_data_cleaned.csv",
    "Algebra A": "data/processed/algebra_a_data_cleaned.csv",
}

st.set_page_config(layout="wide")

# Sidebar: Course Picker
st.sidebar.title("Dashboard Filters")
selected_course = st.sidebar.selectbox("Select Course", list(COURSE_FILES.keys()))

# Load the corresponding data file
data_file = COURSE_FILES[selected_course]
df = pd.read_csv(data_file)

# Sidebar: Additional filters
min_attempts = st.sidebar.slider("Minimum Number of Responses", 0, int(df["num_responses"].max()), 30)
show_extra_columns = st.sidebar.checkbox("Show extra columns (%failed, %giveup)", value=False)

# Optionally filter out bogus wrong_sum entries if computed already
if "wrong_sum" in df.columns:
    df = df[df["wrong_sum"] < 99]

# Apply a filter based on the minimum number of responses
df = df[df["num_responses"] >= min_attempts]

# Compute wrong_sum if not already computed
if "wrong_sum" not in df.columns:
    df["wrong_sum"] = df["%failed1"].fillna(0) + df["%failed2"].fillna(0) + df["%failed3"].fillna(0)

# Build a summary table
summary_table = build_summary_table(df)

# Main view: Display table
st.header(f"Summary for {selected_course}")
if show_extra_columns:
    st.dataframe(summary_table)
else:
    # Display a simpler version (e.g., only showing document_name, pointer, num_responses, Top Wrong Answers)
    st.dataframe(summary_table[["document_name", "pointer", "num_responses", "Top Wrong Answers"]])

# Optionally, add an expander for extra details
with st.expander("Show full data"):
    st.dataframe(df)

# Further visualizations can be added below (e.g., charts based on the summary metrics)
st.header("Visualizations")
st.write("Here you can add interactive charts that slice the data by the selected filters.")

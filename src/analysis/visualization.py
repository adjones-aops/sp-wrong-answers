import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def create_bubble_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates a bubble chart where:
      - x-axis: '%wrong_combined'
      - y-axis: 'num_responses'
      - bubble size: 'total_fails' = (%failed / 100) * num_responses
      - color: 'document_name' if available
      - hover_data: includes 'pointer' and 'top three wrong answers'
    Returns the Plotly figure.
    """
    required_cols = {"%failed", "num_responses", "%wrong_combined"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns for bubble chart: {missing}")

    # Compute total_fails as the actual number of fails
    df = df.copy()
    df["total_fails"] = (df["%failed"].fillna(0) / 100) * df["num_responses"].fillna(0)

    fig = px.scatter(
        df,
        x="%wrong_combined",
        y="num_responses",
        size="total_fails",
        color="document_name" if "document_name" in df.columns else None,
        hover_data=["pointer", "top three wrong answers"],
        title="Bubble Chart: Combined Wrong % vs # of Responses (Bubble size = total fails)",
        labels={"%wrong_combined": "Combined Wrong %", "num_responses": "Number of Attempts"},
    )
    fig.update_traces(marker=dict(sizemin=2, sizemode="area", sizeref=2.0 * max(df["total_fails"]) / (40.0**2)))
    return fig


def show_bubble_chart(df: pd.DataFrame):
    """
    Calls create_bubble_chart and then renders the figure with Streamlit.
    """
    try:
        fig = create_bubble_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    except ValueError as e:
        st.info(str(e))

import pandas as pd
import plotly.graph_objects as go
import pytest

from src.analysis.visualization import create_bubble_chart


@pytest.fixture
def sample_df():
    data = {
        "%failed": [50, 30],
        "num_responses": [100, 200],
        "%wrong_combined": [40, 20],
        "document_name": ["Course A", "Course B"],
        "pointer": ["p1", "p2"],
        "top three wrong answers": ["1) [0] (30%)", "1) [1] (20%)"],
    }
    return pd.DataFrame(data)


def test_create_bubble_chart_returns_figure(sample_df):
    fig = create_bubble_chart(sample_df)
    assert isinstance(fig, go.Figure), "Returned object should be a Plotly Figure"


def test_create_bubble_chart_layout(sample_df):
    fig = create_bubble_chart(sample_df)
    # Check that the title contains expected text
    assert "Bubble Chart" in fig.layout.title.text
    # Check that axis labels are set correctly
    assert fig.layout.xaxis.title.text == "Combined Wrong %"
    assert fig.layout.yaxis.title.text == "Number of Attempts"


def test_create_bubble_chart_trace_data(sample_df):
    fig = create_bubble_chart(sample_df)
    # There should be at least one trace in the figure.
    assert len(fig.data) > 0, "Figure should have at least one trace"

    # Collect x-values from all traces.
    all_x = []
    for trace in fig.data:
        all_x.extend(trace.x)

    expected_x = sample_df["%wrong_combined"].tolist()
    # Sort both lists for comparison.
    assert sorted(all_x) == sorted(expected_x), "x-values in traces should match %wrong_combined values"

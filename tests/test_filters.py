import pandas as pd
import pytest

from src.analysis.summarize import filter_by_num_responses_percentile


@pytest.fixture
def sample_df():
    data = {"pointer": ["p1", "p2", "p3", "p4"], "num_responses": [10, 50, 100, 200]}
    return pd.DataFrame(data)


def test_filter_by_num_responses_percentile(sample_df):
    # For instance, 25th percentile of [10, 50, 100, 200] is 10 (if that is how quantile computes)
    filtered = filter_by_num_responses_percentile(sample_df, percentile=0.25)
    # Depending on distribution, you may expect p1 to be removed if cutoff > 10.
    cutoff = sample_df["num_responses"].quantile(0.25)
    assert all(filtered["num_responses"] >= cutoff)

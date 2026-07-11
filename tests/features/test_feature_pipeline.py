import pytest
import pandas as pd
from src.features.feature_pipeline import get_serving_features

def test_get_serving_features(mocker):
    mock_store = mocker.patch("src.features.feature_pipeline.store")
    mock_data = pd.DataFrame([{
        "click_event_id": 1,
        **{f"I{i}": 0.5 for i in range(1,14)},
        **{f"C{i}": 0.5 for i in range(1,27)},
    }])

    mock_store.get_online_features.return_value.to_df.return_value = mock_data
    entity_rows = [{"click_event_id": 1}]
    res = get_serving_features(entity_rows)
    mock_store.get_online_features.assert_called_once()
    assert res.shape == (1,40)
    assert "click_event_id" in res.columns
    assert "I1" in res.columns
    assert "C26" in res.columns

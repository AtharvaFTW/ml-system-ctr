import pytest
import pandas as pd
from src.training.train import compute_scale_pos_weight


def test_compute_scale_post_weight():
    mock_data = pd.Series([1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1])
    res = compute_scale_pos_weight(mock_data)

    assert res == pytest.approx(2.1666666666666665)

def test_compute_scale_post_weight_no_positives():
    mock_data = pd.Series([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    with pytest.raises(ValueError):
        compute_scale_pos_weight(mock_data)

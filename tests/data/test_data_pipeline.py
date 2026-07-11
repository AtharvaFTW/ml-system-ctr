import pytest
import pandas as pd

from tests.data.test_dummy_data import dummy_data
from src.data.pipeline import split_data

def test_split_data_without_rounding():
    df = pd.DataFrame(dummy_data[:10])
    train_df, val_df, test_df = split_data(df = df, seed = 42)

    assert len(train_df) == 7
    assert len(val_df) == 1
    assert len(test_df) == 2
    assert len(train_df) + len(val_df) + len(test_df) == 10

def test_split_data():
    df = pd.DataFrame(dummy_data)
    train_df, val_df, test_df = split_data(df = df, seed = 42)

    total = len(df)
    assert len(train_df) + len(val_df) + len(test_df) == total
    assert len(train_df) == pytest.approx(total * 0.7, abs = 0.2)
    assert len(val_df) == pytest.approx(total * 0.15, abs = 0.2)
    assert len(test_df) == pytest.approx(total * 0.15, abs = 0.2)

def test_split_no_overlap():
    df = pd.DataFrame(dummy_data)
    train_df, val_df, test_df = split_data(df)

    train_idx = set(train_df.index)
    val_idx = set(val_df.index)
    test_idx = set(test_df.index)

    assert len(train_idx & val_idx) == 0
    assert len(train_idx & test_idx) == 0
    assert len(val_idx & test_idx) == 0
 

# def test_run_pipeline():
#     pass

# def test_push_to_supabase():
#     pass

# def test_features_to_store():
#     pass

# if __name__ == "__main__":
#     test_split_no_overlap()
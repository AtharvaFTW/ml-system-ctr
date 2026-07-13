import pytest
import pandas as pd
import pandera.pandas as pa

from tests.data.test_dummy_data import dummy_data, dummy_data_missing
from src.data.pipeline import (split_data,
                                frequency_encode_categoricals,
                                impute_missing_data,
                                log_transform_integers,
                                load_raw_data,
                                validate_data)

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
 
def test_frequency_encode_categoricals():
    df = pd.DataFrame(dummy_data)
    res = frequency_encode_categoricals(df)
    
    for col in res.columns:
        if col.startswith("C"):
            assert res[col].dtype == "float64"

def test_frequency_encode_categoricals_values():
    df = pd.DataFrame({"C1": ["a", "b" , "a", "a"]})
    res = frequency_encode_categoricals(df)

    assert res["C1"].iloc[0] == pytest.approx(0.75)
    assert res["C1"].iloc[1] == pytest.approx(0.25)


def test_log_transform_integers():
    df = pd.DataFrame(dummy_data)
    res = log_transform_integers(df)

    for col in res.columns:
        if col.startswith("I"):
            assert res[col].dtype == "float64"

def test_log_transform_integers_vlaues():
    df = pd.DataFrame({"I1": [0], "I2":[1]})
    res = log_transform_integers(df)

    assert res["I1"].iloc[0] == pytest.approx(0.0)
    assert res["I2"].iloc[0] == pytest.approx(0.693 , abs = 0.001)


def test_impute_data():
    df = pd.DataFrame(dummy_data_missing)
    res = impute_missing_data(df)

    assert len(df) == len(res)
    for col in res.columns:
        assert res[col].isnull().sum() == 0
    
def test_impute_data_values():
    df = pd.DataFrame({"I1": [0.5, None, 3.4, 0.0, 7.8, None, 2.1, 9.3, 4.6, 6.7]})
    res = impute_missing_data(df)

    assert res["I1"].iloc[1] == 4.3
    assert res["I1"].iloc[5] == 4.3

def test_validate_data_pass():
    df = pd.DataFrame(dummy_data)
    df = df.drop(columns = ["click_event_id","event_timestamp"])

    for col in df.columns:
        if col.startswith("C"):
            df[col] = 12345
    res = validate_data(df)

    assert res is not None

def test_validate_data_fail():
    df = pd.DataFrame([1,2,3,4])

    with pytest.raises(pa.errors.SchemaErrors):
        validate_data(df)


# def test_run_pipeline():
#     pass

# def test_push_to_supabase():
#     pass

# def test_features_to_store():
#     pass

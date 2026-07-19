from fastapi import HTTPException
import pandas as pd
import pytest

from src.serving.schemas import PredictRequest
from src.serving.app import predict
from src.utils.predict_helpers import prepare_features_for_prediction
from tests.data.test_dummy_data import dummy_data

def test_prepare_features_for_prediction():
    df = pd.DataFrame(dummy_data)

    res = prepare_features_for_prediction(df)
    
    required_cols = [f"I{i}" for i in range(1,14)] + [f"C{i}" for i in range(1,27)]

    assert "click_event_id" in df.columns
    assert "click_event_id" not in res.columns
    assert res.columns.tolist() == required_cols


def test_model_not_loaded(mocker):
    mocker.patch("src.serving.app.model_loader.get_model", return_value = None)

    req = PredictRequest(click_event_id= 1)

    with pytest.raises(HTTPException) as exc_info:
        predict(req)

    assert exc_info.value.status_code == 503
import pytest
import pandas as pd
import numpy as np

from src.training.train import compute_scale_pos_weight
from src.training.evaluate import compute_metrics
from src.training.register import get_champion_auc
from src.utils.mlflow_helpers import _get_champion_version

                            


def test_compute_scale_post_weight():
    mock_data = pd.Series([1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1])
    res = compute_scale_pos_weight(mock_data)

    assert res == pytest.approx(2.1666666666666665)

def test_compute_scale_post_weight_no_positives():
    mock_data = pd.Series([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    with pytest.raises(ValueError):
        compute_scale_pos_weight(mock_data)


def test_compute_metrics(mocker):
    mock_model = mocker.Mock()
    mock_model.predict_proba.return_value = np.array([[0.9, 0.1], [0.2, 0.8]])
    mock_model.predict.return_value = np.array([0,1])

    y_test = pd.Series([0,1])

    res = compute_metrics(mock_model, X_test = pd.DataFrame(), y_test = y_test)

    assert res["auc_score"] == 1.0
    assert res["log_loss"] == pytest.approx(0.16425, abs = 1e-4)
    assert res["precision_score"] == 1.0
    assert res["recall_score"] == 1.0


def test_get_champion_auc(mocker):

    mock_client = mocker.Mock()

    mock_version = mocker.Mock()
    mock_version.run_id = "some_run_id"

    mock_model = mocker.Mock()
    mock_model.latest_versions = [mock_version]
    mock_client.search_registered_models.return_value = [mock_model]

    mock_run = mocker.Mock()
    mock_run.data.metrics = {"test_auc": 0.85}
    mock_client.get_run.return_value = mock_run

    mocker.patch("src.training.register.client", mock_client)

    res = get_champion_auc()
    assert res == 0.85

def test_get_champion_auc_no_champion(mocker):
    mock_client = mocker.Mock()
    mock_client.search_registered_models.return_value = []
    mocker.patch("src.training.register.client", mock_client)

    res = get_champion_auc()
    assert res == 0.0


def test_get_champion_version(mocker):
    mock_client = mocker.Mock()
    mock_version = mocker.Mock()
    mock_version.version = 0.1
    
    mock_client.search_model_versions.return_value = [mock_version]

    mocker.patch("src.utils.mlflow_helpers.client", mock_client)
    res= _get_champion_version()
    assert res == 0.1

def test_get_champion_version_no_champion(mocker):
    mock_client = mocker.Mock()
    mock_client.search_model_versions.return_value = []

    mocker.patch("src.utils.mlflow_helpers.client",mock_client)

    res = _get_champion_version()
    assert res is None

# Column drop logic/reorder logic inside /predict in app.py

# def test_run_training():
#     pass

# def test_run_evaluation():
#     pass

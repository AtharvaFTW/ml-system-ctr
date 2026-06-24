from pydantic import BaseModel

class PredictRequest(BaseModel):
    click_event_id : int

class PredictResponse(BaseModel):
    click_probability : float
    prediction : int

class ModelInfoResponse(BaseModel):
    model_name : str
    version : str
    tags : str
    test_auc : float
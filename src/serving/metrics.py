from prometheus_client import Counter, Histogram

PREDICTION_COUNTER = Counter(
    "ctr_predictions_total",
    "Total number of request",
    ["predictions"]
)

PREDICTION_SCORE = Histogram(
    "ctr_prediction_score",
    "Distribution of click probability scores",
    buckets = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

FEATURE_RETRIEVAL_LATENCY = Histogram(
    "ctr_feature_retrieval_latency",
    "Latency tracking Feast/Redis call duration",
    buckets = [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]    
)

MODEL_INFERENCE_LATENCY = Histogram(
    "ctr_model_inference_latency",
    "Latency tracking model inference duration",
    buckets = [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)
# CTR Prediction — Machine Learning End-to-End System

## Phase 1 — Data Pipeline

### What it does?
Ingests the raw Criteo CTR dataset, validates the schema, preprocesses features, handles class imbalance, splits into train/val/test, and stores processed features to PostgreSQL (via Supabase)

### Dataset
- Development: reczoo/Criteo_x1 from HuggingFace (2.39GB, CSV Format)
- Production: criteo/CriteoClickLogs from HuggingFace (full dataset, Parquet format)
- Switch datasets requires only a config change — pipeline logic is dataset-agnostic

### Inputs
- `data/raw/train.csv` - raw Criteo dataset

### Outputs
- `data/processed/train.parquet` 
- `data/processed/val.parquet`
- `data/processed/test.parquet`
- validation report logged to stdout

### Data flow
raw CSV -> schema validation -> missing value imputation -> feature encoding -> train/val/test split -> parquet storage

### Key decisions
- Pandera for validation — lightweight, Pythonic , fails loudly.
- Supabase(free tier) — Eliminates the overhead of local PostgreSQL.
- scale_pos_weight over SMOTE — Criteo has 26 high-cardinality categorical features, SMOTE interpolation is meaningless on hashed categoricals.
- Mean imputation for integer features, 'missing' token for categoricals.
- Fixed random seed (42) for reproducibility.

---
## Phase 2 — Feast Feature Store

### What it does?
The feast feature store reduces and eliminates the training-serving skew. What is training-serving skew? The data mismatch between what model saw while training and what it is seeing during inference.

- Offline store - historical features for training. Reads from the parquet files mentioned below.
- Online store - real-time features for inference. Reads from the Redis cache (fast, in-memory).

### Inputs
- `data/processed/train.parquet` - processed train data
- `data/processed/val.parquet` - processed val data
- `data/processed/test.parquet` - processed test data

### Outputs
- Feature definitions in code `src/features`
- Feast registry file `feature_store.yaml`
- A script that pushes features to the store.
- A training retrieval function.
- An online retrieval function.

### Data flow
```
parquet_files → Feast offline store → training_features
                        ↓
                feast materialize (the command that syncs features from offline → online)
                        ↓
                Feast online store (Redis) → inference features
```

---
## Phase 3 — Airflow DAG (In Progress)

### What it does?
Airflow has two components, DAG and Task. Let's see each one does:

- DAG — Directed Acyclic Graph. It's a sequence of steps where each step flows into next, no loops (acyclic). In Airflow, your entire training pipeline is one DAG.

- Task — One single step inside a DAG. Each step in the data flow is one Task. A task is just a Python fucntion that Airflow runs.
Key property: each **Task is independently retryable**. If `train_model` fails, Airflow reruns just `train_model`, not the whole DAG from start.

### Inputs
- Processed feature data from Feast offline store (Supabase)
- `data/processed/train.parquet`— for validation step

### Outputs
- Evaluation metrics logged to MLFlow (AUC-ROC, log loss, precision, recall)
- Trained XGBoost model artifact registered in MLFlow model register (only if AUC-ROC beats the current champion model).

### Data flow
```
validate_data → retrieve_features → train_model → evaluate model → register_model
```
### Key decisions
- Each task is independently retryable — failure in one task doesn't restart the whole DAG
- DAG is idempotent — running twice with same data produces same result
- Model only registers if AUC-ROC beats the current champion — no accidental downgrades!

---
## Phase 4 — Model Training & Experiment Tracking

### What it does?
In this phase we cover 2 things:
- Train our XGBoost model on CTR dataset.
- MLFlow experiment tracking — tracks our training hyperparameters/ logs and model state_dict as model artifact.

We will execute this phase via the Airflow DAG

### Inputs
- Training features retrieved from Feast offline store (Supabase)
   - I1-I13 integer features (log transformed)
   - C1-C26 categorical features (frequency encoded)
   - `label` column (0/1 click labels)

- `data/processed/train.parquet` — training split
- `data/processed/val.parquet` — validation split for early stopping

### Outputs
- Trained XGBoost model artifact saved to MLFlow
- Experiment run logged to MLFlow with:
  - Hyperparameters (n_estimators, max_depth, scale_pos_weight, etc.)
  - Metrics (AUC-ROC, log loss, precision, recall)
  - Dataset hash (for reproducibility)
  - Feast feature view version used
- Model tagged as `challenger` in MLFlow registry
- Promoted to `champion` if AUC-ROC beats the current champion

### Data flow
```
Feast offline store (Supabase)
        ↓
retrieve_features (Airflow task)
        ↓
train_model (XGBoost training with scale_pos_weight)
        ↓
evaluate_model ( AUC-ROC , log loss, precision , recall on test set)
        ↓
MLFlow (log hyperparameters, metrics, model artifact)
        ↓
register_model (champion/ challenger comparision)
        ↓
MLFlow Model Registry (tagged champion or challenger)
```

### Key decisions
- XGBoost **>** Neural Networks — XGBoost is lighter, trains on CPU and works well with binary classification.
- scale_pos_weight **>** SMOTE — SMOTE creates dummy data to eliminate the imbalance, which adds noise to our training data on the other hand scale_pos_weight handles the imbalance by giving more importance to the minority class and doesn't modify our data.
- MLFlow **>** W&B — MLFLow is open source and runs locally with no account or api required. W&B has free tier but limited to 5GB space. For self-hosted system MLFLow is right default. At scale, internal tools like Vizier or VertexAI replaces both.

---
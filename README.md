# CTR Prediction — Machine Learning End-to-End System

## Phase 1 — Data Pipeline (Completed)

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

## Phase 2 - Feast Feature Store (In Progress)

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


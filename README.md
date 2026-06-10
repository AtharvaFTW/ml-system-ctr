# CTR Prediction — Machine Learning End-to-End System

## Phase 1 — Data Pipeline (In Progress)

### What it does?
Ingests the raw Criteo CTR dataset, validates the schema, preprocesses features, handles class imbalance, splits into train/val/test, and stores processed features to PostgreSQL (via Supabase)

### Inputs
- `data/raw/train.txt` - raw Criteo dataset (tab-separated, no header)

### Outputs
- `data/processed/train.parquet` 
- `data/processed/val.parquet`
- `data/processed/test.parquet`
- validation report logged to stdout

### Data flow
raw CSV -> schema validation -> missing value imputation -> feature encoding -> train/val/test split -> parquet storage

### Key decisions
- Pandera for validation — lightweight, Pythonic , fails loudly.
- Supabase(free tier) — Eliminates the overhead of local PostgreSQL
- scale_pos_weight over SMOTE — Criteo has 26 high-cardinality categorical features, SMOTE interpolation is meaningless on hashed categoricals.
- Mean imputation for integer features, 'missing' token for categoricals.
- Fixed random seed (42) for reproducibility.
# Phase 1 — Data Pipeline Flow

## Data Flow

```
data/raw/train.txt
        |
        v
[1. Ingestion ]
- Load tab-seperated file
- Assign colum names (label, I1-I12, C1-C26)
- Log shape and first few rows
        |
        v
[2. Validation — Pandera ]
- Check column count (40 columns)
- Check label is 0 or 1
- Check integer features are numeric
- Check for unexpected nulls
- FAIL LOUDLY if any check fails
        |
        v
[3. Missing Value Imputation ]
- Integer features (I1-I13): fill with column mean
- Categorical features (C1-C26): fill with string 'missing'        
        |
        v
[4. Feature Engineering ]
- Frequency encode categorical features
- Log transform integer features (handle skew)
        |
        v
[5. Train / Val / Test Split]
- 70% train, 15% val, 15% test
- Fixed seed = 42
- Log class distribution for each split
        |
        v
[6. Storage]
- Save to data/processed/train.parquet
- Save to data/processed/val.parquet
- Save to data/processed/test.parquet
- Save processed features to PostgreSQL (Supabase)
```
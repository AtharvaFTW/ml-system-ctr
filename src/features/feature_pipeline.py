from feast import FeatureStore
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone

from src.features.feature_definitions import get_entity, get_data_source, get_integer_feature_view, get_categorical_feature_view
from src.logger import get_logger

logger = get_logger(__name__)

entity = get_entity()
source = get_data_source("train_features")
integer_fv = get_integer_feature_view(source, entity)
categorical_fv = get_categorical_feature_view(source, entity)

all_features = [f"integer_features:I{i}" for i in range(1,14)] + \
                [f"categorical_features:C{i}" for i in range(1,27)]

try:
    logger.info("Initializing the Feature Store...")
    store = FeatureStore(repo_path= Path("src/features/"))
    logger.info("✔ Store initialized!")
except Exception as e:
    logger.info(f"Store initialization failed: {e}")
    raise

def push_features_to_store():
    """
    Pushes features from Supabase to Feast offline store and materializes to Redis online store.
    """
    try:
        logger.info("Applying the feature definitions to Feast store...")
        store.apply([entity, integer_fv, categorical_fv])

        logger.info("Materializing features to Redis...")
        store.materialize_incremental(end_date = datetime.now(timezone.utc))
        logger.info("✔ Features materialized successfully!")

    except Exception as e:
        logger.error(f"❌ Failed to apply feature definitions and materialization: {e}")
        raise

def get_training_features(entity_df: pd.DataFrame, features: list = all_features) -> pd.DataFrame:
    """
    Retrieves point-in-time correct features for training.

    Args:
        store: Feast feature store
        entity_df: DataFrame with click_event_id and event_timestamp
        features: 

    Returns:
        DataFrame with all features for training.
    """
    
    try:
        logger.info("Pulling historical features...")
        data = store.get_historical_features(
            entity_df = entity_df,
            features = features
        ).to_df()

        if not data.empty:
            logger.info("✔ Pulled historical figures successfully!")
            logger.info(f"Trainig Features shape: {data.shape}")
        else:
            logger.warning(f"? Training data is empty!")

    except Exception as e:
        logger.error(f"❌ Pull failed: {e}")
        raise

    return data
    

def get_serving_features(entity_rows: list, features: list = all_features) -> dict:
    """
    Retrieves features for a single inference request from Redis.

    Args:
        entity_rows: list of dicts with click_event_id

    Returns:
        dict of feature values
    """
    logger.info("Pulling serving features...")
    try:
        data = store.get_online_features(
            features = features,
            entity_rows = entity_rows
        ).to_df()
        if not data.empty:
            logger.info("✔ Pulled serving features successfully!")
            logger.info(f"Serving features shape: {data.shape}")
        else:
            logger.warning(f"? Serving data is empty!")

    except Exception as e:
        logger.error(f"❌ Pull failed: {e}")
        raise

    return data

if __name__ == "__main__":
    push_features_to_store()
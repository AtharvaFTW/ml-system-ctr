from feast import Entity, FeatureView, Field
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource
from feast.types import Float32, Int64
from feast.value_type import ValueType
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

def get_entity():
    """
    Defines the click event entity
    Each row in Criteo represents one ad display event.

    Returns:
        Entity: click_event_id entity
    """
    
    return Entity(name = "click_event_id",
                    value_type= ValueType.INT64)

def get_data_source(table_name: str):
    """
    Defines the PostgreSQL data source for Feast.

    Args:
        table_name: Supabase table_name to read from

    Returns:
        PostgreSQLSource
    """
    return PostgreSQLSource(
        table = table_name,
        timestamp_field= "event_timestamp"
    )

def get_integer_feature_view(source, entity):
    """
    Feature view for I1-I13 integer features.

    Args:
        source: data source
        entity: click_event_id entity
    
    Returns:
        FeatureView
    """
    return FeatureView(
        name = "integer_features",
        entities = [entity],
        schema = [Field(name = f"I{i}",dtype = Float32) for i in range(1,14)],
        source = source,
        ttl = timedelta(days=1)
    )

def get_categorical_feature_view(source, entity):
    """
    Feature view for C1-C26 categorical features.

    Args:
        source: data source
        entity: click_event_id entity
    
    Returns:
        FeatureView
    """
    return FeatureView(
        name = "categorical_features",
        entities = [entity],
        schema = [Field(name = f"C{i}",dtype = Int64) for i in range(1,27)],
        source = source,
        ttl = timedelta(days=1)
    )
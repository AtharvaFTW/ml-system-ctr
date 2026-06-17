from feast import Entity, FeatureView, Field
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource
from feast.types import Float32, Int64

def get_entity():
    """
    Defines the click event entity
    Each row in Criteo represents one ad display event.

    Returns:
        Entity: click_event_id entity
    """
    
    return Entity("click_event_id")

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
    pass

def get_categorical_feature_view(source, entity):
    """
    Feature view for C1-C26 categorical features.

    Args:
        source: data source
        entity: click_event_id entity
    
    Returns:
        FeatureView
    """
    pass
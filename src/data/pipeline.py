from sklearn.model_selection import train_test_split
from pathlib import Path
from datasets import load_dataset
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging
import pandas as pd
import pandera.pandas as pa
import numpy as np
import os


load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DB_URL)

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.WARNING)
logging.getLogger("datasets").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

def load_raw_data(filepath: str = None, n_rows: int = None) -> pd.DataFrame:
    """
    Load a raw Criteo dataset from huggingface.

    Args:
        filepath: path to raw csv file.
        nrows: number of rows to load, None loads all rows

    Returns:
        DataFrame with colums: label, I1-I13 and C1-C26

    Raises:
        FileNotFoundError: if filepath does not exist (if provided) 
    """

    if not filepath:
        try:
            logger.info("Using HuggingFace to load dataset...")
            dataset = load_dataset("reczoo/Criteo_x1", split= "train")
            df = dataset.to_pandas()
            if n_rows:
                df = df.head(n_rows)
            logger.info(f"Dataset shape: {dataset.shape}")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            raise

    else:
        try:     
            filepath = Path(filepath)
            if filepath.exists():
                logger.info(f"Using {filepath} to load dataset...")
                dataset = pd.read_csv(filepath, nrows = n_rows)
                logger.info(f"Dataset shape: {dataset.shape}")
            else:
                logger.error(f"❌ File not found: {filepath}")
                raise FileNotFoundError(f"❌ File not found: {filepath}")
        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error: {e}")
            raise

    
    logger.info("Dataset Loaded!")
    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate raw dataframe schema using Pandera.
    Fails loudly if any checks fail — pipeline stops immediately.

    Args:
        df: Raw df returned by the load_raw_data()

    Returns:
        validated df, identical to the input if all the checks are passed

    Raises:
        pandera.errors.SchemaError: if validation fails 
    """
    schema = pa.DataFrameSchema(
        {
            "label": pa.Column(int, pa.Check.isin([0,1]), nullable= False),
            r"I\d+$": pa.Column(float, regex= True, nullable= True),
            r"C\d+$": pa.Column(int, regex= True, nullable= True)
            
        },
        strict = True
    )
    try:
        logger.info("Validating the data...")
        schema.validate(df)
        logger.info("✔ Validation passed successfully!")

    except pa.errors.SchemaError as e:
        logger.error(f"❌ Validation failed with: {e}")
        raise
        
    return df

def impute_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles the missing values explicitly.
    - Integer Features (I1 - I13): fill with the column mean.
    - Categorical Features (C1 - C26): replace with 0 (hased integers, no string replacement).

    Args:
        df: validated dataframe returned from validate_data()

    Returns:
        df with no missing values/ fields.
    """
    if not df.isnull().any().any():
        logger.info("Found no missing values")
        return df

    else:
        try:
            logger.info("Imputing missing values...")
            i_cols = [col for col in df.columns if col.startswith("I")]
            c_cols = [col for col in df.columns if col.startswith("C")]
            
            for col in i_cols:
                df[col] = df[col].fillna(df[col].mean())
            for col in c_cols:
                df[col] = df[col].fillna(0)

        except Exception as e:
            logger.error("❌ Imputation Failed !")
            raise 

        logger.info("✔ Imputed missing data successfully !")
        return df

def frequency_encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace each categorical value with it's frequency in the column.

    Args:
        df: Dataframe returned by impute_missing_data()

    Returns:
        df with categorical values replaced with float(frequencies)
    """
    logger.info("Frequency encoding the C features...")

    try:
        c_cols = [col for col in df.columns if col.startswith("C")]
        for col in c_cols:
            freq = df[col].value_counts(normalize= True)
            df[col] = df[col].map(freq)
        logger.info("✔ Frequency encoding completed successfully!")

    except Exception as e:
        logger.error(f"❌ Frequency encoding failed: {e}")
        raise

    return df

def log_transform_integers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Log transform the int values in (I1- I13) into uniform range.
    Uses log1p to handle zeros safely

    Args:
        df: Dataframe returned by frequency_encode_categoricals()
    
    Returns:
        df with log-transformed int features
    """
    logger.info("Log transforming the I features...")
    try:
        i_cols = [col for col in df.columns if col.startswith("I")]
        for col in i_cols:
            df[col] = np.log1p(df[col])
        logger.info("✔ Log trasformation completed successfully!")
    
    except Exception as e:
        logger.error(f"❌ Log transformation failed: {e}")
        raise
    
    return df

def split_data(df: pd.DataFrame, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split the dataset into train, validation and test sets.
    Default ratio = 70:15:15.
    Log class distribution after each split.

    Args:
        df: fully processed dataframe
        seed: random seed for reproducibility
    
    Returns:
        tuple of (train_df, val_df, test_df)
    """
    logger.info("Splitting the data into train/val/test")
    try:
        train_df, test_df = train_test_split(df, test_size= 0.3, random_state= seed)
        val_df, test_df = train_test_split(test_df, test_size= 0.5, random_state= seed)
        logger.info(f"Train shape: {train_df.shape}")
        logger.info(f"Validation shape: {val_df.shape}")
        logger.info(f"Test shape: {test_df.shape}")

        for name, split in [("Train",train_df),("Val", val_df), ("Test", test_df)]:
            dist = split["label"].value_counts(normalize = True)
            logger.info(f"{name} class distribution: \n{dist}")

        logger.info("✔ Dataset split successfully!")

    except Exception as e:
        logger.error(f"❌ Splitting failed: {e}")
        raise

    return (train_df, val_df, test_df)


def save_splits(train_df:pd.DataFrame, val_df: pd.DataFrame, test_df:pd.DataFrame, output_dir: str) -> None:
    """
    Saves the train, val, test splits as parquet files.

    Args:
        train_df: training split
        val_df: validation split
        test_df: test split 
        save_dir: location to save the parquet files

    Returns:
        None
    """
    logger.info(f"Saving the df splits as paraquets at {output_dir}...")

    try:
        Path(output_dir).mkdir(parents= True, exist_ok= True)
        train_df.to_parquet(Path(output_dir)/ "train.parquet")
        val_df.to_parquet(Path(output_dir)/"val.parquet")
        test_df.to_parquet(Path(output_dir)/"test.parquet")
        logger.info(f"✔ Save successful!")
    except Exception as e:
        logger.error(f"❌ Save Failed: {e}")
        raise

def push_to_supabase(df: pd.DataFrame, table_name: str)-> None:
    """
    Loads the parquet files to the PostgreSQL (via Supabase).

    Args:
        df: processed dataframe
        table_name: table to insert data

    Returns:
        None
    """
    logger.info(f"Pushing the df to {table_name}...")
    try:
        df.sample(10000).to_sql(table_name, engine, if_exists="replace",index= False, method = "multi", chunksize = 1000)
        logger.info(f"✔ Successfully pushed {len(df)} rows to {table_name}!")

    except Exception as e:
        logger.error(f"Push failed: {e}")
        raise
    

def run_pipeline(raw_filepath:str= None, n_rows: int = None , output_dir: str = r"data/processed") -> None:
    """
    Orchestrates the full data pipeline end to end.
    Calls each step in order. Fails loudly if any step fails.

    Args:
        raw_filepath: path to raw train.csv if available else fetches from Huggingface (reczoo/Criteo_x1).
        output_dir: location to save the processed parquet files.
        n_rows: number of rows to load, None loads all

    Returns:
        None
    """
    logger.info("Firing the data pipeline ...")

    try:

        data = load_raw_data(filepath= raw_filepath, n_rows = n_rows)
        data = validate_data(data)
        data = impute_missing_data(data)
        data = frequency_encode_categoricals(data)
        data = log_transform_integers(data)
        train_data, val_data, test_data = split_data(data)
        save_splits(train_data, val_data, test_data, output_dir)
        push_to_supabase(train_data, "train_features")
        push_to_supabase(val_data, "val_features")
        push_to_supabase(test_data, "test_features")

        logger.info("✅ Datapipeline executed Successfully!")

    except Exception as e:
        logger.error(f"Data pipeline failed: {e}")
        raise
    

if __name__ == "__main__":
    
    run_pipeline( n_rows= 1000001,output_dir= r"data/processed")
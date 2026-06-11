from datasets import load_dataset
import pandas as pd

def download_criteo_dataset(output_dir: str) -> None:
    """
    Downloads the Criteo x1 sample from Hugging Face.
    Saves as train.csv in output_dir.

    Args:
        output_dir: directory to save the downloaded dataset

    Returns:
        None
    
    Raises:
        Exception if download fails
    """
    pass
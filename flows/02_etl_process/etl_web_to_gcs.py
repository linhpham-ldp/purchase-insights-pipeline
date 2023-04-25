from pathlib import Path
from typing import List
import os
import pandas as pd
import kaggle
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint

os.environ['KAGGLE_USERNAME'] = 'linhphamldp'
os.environ['KAGGLE_KEY'] = '~/kaggle/'


@task(retries=3)
def download_data(kaggle_bucket: str, output_dir: str) -> str:
    """
    Download data from Kaggle
        
    Args:
        kaggle_bucket: The bucket (typically displayed in the web url after https://www.kaggle.com/datasets/) 
        output_dir: The directory to save the downloaded file(s) in

    Returns:
        The path to the downloaded file
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      
    # Download the data and save it to the output directory
    raw_file = kaggle.api.dataset_download_files(kaggle_bucket, path=output_dir)
    
    # Return the path to the downloaded file
    return os.path.join(output_dir, raw_file)

@task(log_prints=True)
def extract_data(raw_file: str, output_dir: str) -> List[str]:
    """
    Extract the downloaded data from a zip file
        
    Args:
        zip_file: The path to the downloaded zip file
        output_dir: The directory to save the extracted files in

    Returns:
        A list of paths to the extracted files
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract the files from the zip file
    with zipfile.ZipFile(raw_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    # Get a list of the extracted file paths
    extracted_files = []
    for file_name in os.listdir(output_dir):
        if file_name.endswith('.csv'):
            extracted_files.append(os.path.join(output_dir, file_name))
    
    # Return the list of extracted file paths
    return extracted_files


@task(log_prints=True)
def compress_file(input_files: List[str], output_dir: str, compression_type: str) -> List[str]:
    """
    Compress a list of files using gzip
        
    Args:
        input_files: A list of input file paths
        output_dir: The directory to save the compressed output files
        compression_type: The compression type to use

    Returns:
        A list of paths to the compressed files
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Compress each input file
    compressed_files = []
    for input_file in input_files:
        # Get the output file name by adding the compression type extension to the input file name
        output_file = os.path.join(output_dir, os.path.basename(input_file) + '.' + compression_type)

        # Compress the file using gzip format
        with open(input_file, 'rb') as f_in:
            with gzip.open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Add the path to the compressed file to the list
        compressed_files.append(output_file)

    # Return the list of compressed file paths
    return compressed_files


# @task()
# def write_gcs(path: Path) -> None:
#     """Upload local parquet file to GCS"""
#     gcs_block = GcsBucket.load("zoom-gcs")
#     gcs_block.upload_from_path(from_path=path, to_path=path)
#     return


@flow()
def etl_web_to_gcs(kaggle_bucket: str, output_dir: str) -> List[str]:
    """The main ETL function"""
 
    raw_file_path = download_data(kaggle_bucket, output_dir)
    extracted_file_list = extract_data(raw_file_path, output_dir)
    compressed_files = compress_file(extracted_file_list, output_dir)
    # write_gcs(path)


if __name__ == "__main__":
    kaggle_bucket = "mkechinov/ecommerce-behavior-data-from-multi-category-store"
    output_dir = "data"
    bucket_name = "purchase-data-01"
    etl_web_to_gcs(kaggle_bucket, output_dir)

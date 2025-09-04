import os
import shutil
import sys
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
from book_recommender.logger.log import logger
from book_recommender.config.configuration import WebAppConfiguration
from book_recommender.exception.exception_handler import BookRecommenderException


class DataIngestion:
    def __init__(self, config = WebAppConfiguration()):
        """
            Data Ingestion Component
        """
        try:
            self.config = config.get_data_ingestion_config()
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore

    def download_dataset(self):
        """
            Download dataset from Kaggle
        """
        try:
            dataset_url = self.config.dataset_url
            raw_data_dir = self.config.raw_data_dir
            os.makedirs(raw_data_dir, exist_ok=True)
            ingested_dir = self.config.ingested_dir


            # Initialize API
            api = KaggleApi()
            api.authenticate()  # Reads from ~/.kaggle/kaggle.json

            # Destination path
            output_path = os.path.expanduser(raw_data_dir)
            logger.info(f"⬇️ Downloading dataset from {dataset_url} to {output_path}")
            # Download dataset (same as your curl URL)
            api.dataset_download_files(
                dataset=dataset_url,
                path=output_path,
                unzip=True  # keep as .zip, set to True if you want extracted
            )
            logger.info(f"✅ Dataset downloaded to: {output_path}")

        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore

    def extract_usefull_files(self):
        """
            Extract useful files from the downloaded dataset
        """
        try:
            raw_data_dir = self.config.raw_data_dir
            ingested_dir = self.config.ingested_dir
            os.makedirs(ingested_dir, exist_ok=True)

    
            logger.info(f"📦 Extracting useful files from {self.config.raw_data_dir}")
            # Implement your extraction logic here
            # move only important file in the ingested_dir
            for file in os.listdir(raw_data_dir):
                if file.endswith(".csv"):  
                    shutil.copy(os.path.join(raw_data_dir, file), os.path.join(ingested_dir, file))
            logger.info(f"✅ Useful files extracted to: {ingested_dir}")

        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore

    def initiate_data_ingestion(self):
        """
            Initiate data ingestion process
        """
        try:
            logger.info(f"--> Data Ingestion log started")
            self.download_dataset()
            self.extract_usefull_files()
            logger.info(f"--> Data Ingestion log completed")

        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore

import os
import sys
from book_recommender.constants import *
from book_recommender.utils.util import read_yaml_file
from book_recommender.entity.config_entity import DataIngestionConfig
from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from pathlib import Path

class WebAppConfiguration:
    def __init__(self,config_file_path:str = CONFIG_FILE_PATH):
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
        
        except Exception as e:
            raise WebAppException(e,sys) from e #type:ignore
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir = self.config_info['artifact_config']['artifacts_dir']
            data_ingestion_dir = os.path.join(artifact_dir, "data_ingestion")
            dataset_download_url = self.config_info['data_ingestion_config']['dataset_download_url']

            raw_data_dir = os.path.join(data_ingestion_dir, self.config_info['data_ingestion_config']['raw_data_dir'])
            ingested_dir = os.path.join(data_ingestion_dir, self.config_info['data_ingestion_config']['ingested_dir'])

            data_ingestion_config_response = DataIngestionConfig(
                root_dir=Path(data_ingestion_dir),
                dataset_url=dataset_download_url,
                raw_data_dir=Path(raw_data_dir),
                ingested_dir=Path(ingested_dir)
            )
            logger.info(f"Data Ingestion config: {data_ingestion_config_response}")
            return data_ingestion_config_response

        except Exception as e:
            raise WebAppException(e,sys) from e #type:ignore
        

import os
import sys
from book_recommender.constants import *
from book_recommender.utils.util import read_yaml_file
from book_recommender.entity.config_entity import (DataIngestionConfig, 
                                                    DataValidationConfig, 
                                                    DataTransformationConfig,
                                                    ModelTrainingConfig,
                                                    RecommendationConfig)
from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from pathlib import Path

class WebAppConfiguration:
    def __init__(self,config_file_path:str = CONFIG_FILE_PATH):
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
        
        except Exception as e:
            raise BookRecommenderException(e,sys) from e #type:ignore
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir = self.config_info['artifact_config']['artifacts_dir']
            os.makedirs(artifact_dir, exist_ok=True)
            dataset_dir = self.config_info['data_ingestion_config']['dataset_dir']
            data_ingestion_dir = os.path.join(artifact_dir,dataset_dir)
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
            raise BookRecommenderException(e,sys) from e #type:ignore

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            artifact_dir = self.config_info['artifact_config']['artifacts_dir']
            dataset_dir = self.config_info['data_ingestion_config']['dataset_dir']
            data_validation_dir = os.path.join(artifact_dir,dataset_dir)

            clean_data_dir = os.path.join(data_validation_dir, 
                                          self.config_info['data_validation_config']['clean_data_dir'])
            serialized_object_dir = os.path.join(artifact_dir, 
                                                 self.config_info['data_validation_config']['serialized_object_dir'])

            book_file_csv_path = os.path.join(artifact_dir, dataset_dir,
                                               self.config_info['data_ingestion_config']['ingested_dir'],
                                               self.config_info['data_validation_config']['books_file'])
            
            ratings_file_csv_path = os.path.join(artifact_dir, dataset_dir,
                                               self.config_info['data_ingestion_config']['ingested_dir'],
                                               self.config_info['data_validation_config']['ratings_file'])
            
            data_validation_config_response = DataValidationConfig(
                clean_data_dir= Path(clean_data_dir),
                serialized_object_dir= Path(serialized_object_dir),
                books_file=book_file_csv_path,
                ratings_file=ratings_file_csv_path,
            )
            logger.info(f"Data Validation config: {data_validation_config_response}")
            return data_validation_config_response

        except Exception as e:
            raise BookRecommenderException(e,sys) from e #type:ignore
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            artifact_dir = self.config_info['artifact_config']['artifacts_dir']
            dataset_dir = self.config_info['data_ingestion_config']['dataset_dir']
            data_transformation_dir = os.path.join(artifact_dir,dataset_dir)

            transformed_data_dir = os.path.join(data_transformation_dir, 
                                          self.config_info['data_transformation_config']['transformed_data_dir'])
            clean_data_file_path = os.path.join(artifact_dir, dataset_dir,
                                          self.config_info['data_validation_config']['clean_data_dir'],'clean_data.csv')
            data_transformation_config_response = DataTransformationConfig(
                transformed_data_dir= Path(transformed_data_dir),
                clean_data_file_path= Path(clean_data_file_path)
            )
            logger.info(f"Data Transformation config: {data_transformation_config_response}")
            return data_transformation_config_response
        
        except Exception as e:
            raise BookRecommenderException(e,sys) from e #type:ignore
        
    def get_model_training_config(self) -> ModelTrainingConfig:
        try:
            artifact_dir = self.config_info['artifact_config']['artifacts_dir']
            dataset_dir = self.config_info['data_ingestion_config']['dataset_dir']

            transformed_data_file_path = os.path.join(artifact_dir,dataset_dir,
                                                     self.config_info["data_transformation_config"]["transformed_data_dir"],
                                                     "book_pivot.pkl")
            trained_model_dir = os.path.join(artifact_dir, 
                                          self.config_info['model_training_config']['trained_model_dir'])
            model_file = self.config_info['model_training_config']['model_file']

            model_training_config_response = ModelTrainingConfig(
                transformed_data_file_path= Path(transformed_data_file_path),
                trained_model_dir= Path(trained_model_dir),
                trained_model_name= model_file
            )
            logger.info(f"Model Training config: {model_training_config_response}")
            return model_training_config_response
        
        except Exception as e:
            raise BookRecommenderException(e,sys) from e #type:ignore
    
    def get_recommendation_config(self) -> RecommendationConfig:
        try:
            artifact_dir = self.config_info["artifact_config"]["artifacts_dir"]

            trained_model_name = self.config_info["recommendation_config"]["trained_model_name"]
            
            trained_model_path = os.path.join(artifact_dir,
                                                self.config_info["model_training_config"]["trained_model_dir"],
                                                trained_model_name)

            book_pivot_serialized_file = os.path.join(artifact_dir,
                                                self.config_info["data_validation_config"]["serialized_object_dir"],
                                                self.config_info["recommendation_config"]["book_pivot_serialized_file"])
            
            final_rating_serialized_file = os.path.join(artifact_dir,
                                                self.config_info["data_validation_config"]["serialized_object_dir"],       
                                                self.config_info["recommendation_config"]["final_rating_serialized_file"])
            
            book_name_serialized_file = os.path.join(artifact_dir,
                                                self.config_info["data_validation_config"]["serialized_object_dir"],       
                                                self.config_info["recommendation_config"]["book_name_serialized_file"])
            
            recommendation_config_response = RecommendationConfig(
                book_pivot_serialized_file= Path(book_pivot_serialized_file),
                final_rating_serialized_file= Path(final_rating_serialized_file),
                book_name_serialized_file= Path(book_name_serialized_file),
                trained_model_path= Path(trained_model_path),
                trained_model_name= trained_model_name,
                num_recommendations= self.config_info["recommendation_config"]["num_recommendations"]
            )
            logger.info(f"Recommendation config: {recommendation_config_response}")
            return recommendation_config_response
        
        except Exception as e:
            raise BookRecommenderException(e,sys) from e #type:ignore
                                              
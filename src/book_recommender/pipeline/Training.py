from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from book_recommender.components.stage_0_data_ingestion import DataIngestion
from book_recommender.components.stage_1_data_validation import DataValidation
from book_recommender.components.stage_2_data_transformation import DataTransformation
import sys

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.data_transformation = DataTransformation()

    def run(self):
        try:
            logger.info(f"{'='*20} Training pipeline started {'='*20}")
            self.data_ingestion.initiate_data_ingestion()
            self.data_validation.initiate_data_validation()
            self.data_transformation.initiate_data_transformation()
            logger.info(f"{'='*20} Training pipeline completed {'='*20}\n\n")
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore
        

from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from book_recommender.components.stage_0_data_ingestion import DataIngestion
from book_recommender.components.stage_1_data_validation import DataValidation
from book_recommender.components.stage_2_data_transformation import DataTransformation
from book_recommender.components.stage_3_model_training import ModelTrainer
import sys

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()
        self.methods = {
            "Data Ingestion": self.data_ingestion.initiate_data_ingestion,
            "Data Validation":self.data_validation.initiate_data_validation,
            "Data Transformation":self.data_transformation.initiate_data_transformation,
            "Model Training":self.model_trainer.initiate_model_training,
        }
     
    def run(self):
        logger.info(f"{'='*20} Training pipeline started {'='*20}")
        for name, method in self.methods.items():
            try:
                logger.info(f"Starting {name}...")
                yield f"data: {name} started 🚀\n\n"

                method()  # run the actual step

                logger.info(f"{name} completed")
                yield f"data: {name} completed ✅\n\n"
            except Exception as e:
                yield f"data: {name} failed ❌\n\n"
                raise BookRecommenderException(e, sys) from e #type:ignore
            
        logger.info(f"{'='*20} Training pipeline completed {'='*20}")
        yield "Training completed 🎉\n\n"
        
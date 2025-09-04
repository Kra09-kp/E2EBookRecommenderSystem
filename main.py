from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from book_recommender.pipeline.DataIngestion import DataIngestionPipeline
import sys

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info("*"*20)
    logger.info(f"--> {STAGE_NAME} started")
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.run()
    logger.info(f"--> {STAGE_NAME} completed")
    logger.info("*"*20)

except Exception as e:
    logger.error(f"Error occurred: {e}")
    raise BookRecommenderException(e, sys) from e #type: ignore


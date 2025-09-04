from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from book_recommender.components.stage_0_data_ingestion import DataIngestion

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def run(self):
        try:
            logger.info(f"{'='*20} {STAGE_NAME} {'='*20}")
            data_ingestion = DataIngestion()
            data_ingestion.initiate_data_ingestion()
            logger.info(f"{'='*20} {STAGE_NAME} completed {'='*20}\n\n")
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore
        
if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
    pipeline.run()
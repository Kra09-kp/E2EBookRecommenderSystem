from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from book_recommender.pipeline.Training import TrainingPipeline

pipeline = TrainingPipeline()
pipeline.run()
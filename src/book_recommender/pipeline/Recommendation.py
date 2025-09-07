from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from book_recommender.components.stage_4_recommendation import RecommendationEngine
import sys

class RecommendationPipeline:
    def __init__(self):
        self.recommendation_engine = RecommendationEngine()

    def recommend_books(self, book_name):
        try:
            print("\n\n")
            logger.info(f"{'='*10} Recommendation pipeline started {'='*10}")
            recommendations = self.recommendation_engine.recommend_books(book_name)
            logger.info(f"Recommendations for book {book_name}: {recommendations}")
            logger.info(f"{'='*10} Recommendation pipeline completed {'='*10}\n\n")
            return recommendations
        except Exception as e:
            raise BookRecommenderException(e, sys) from e  # type:ignore
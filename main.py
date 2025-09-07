from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger
from book_recommender.pipeline.Training import TrainingPipeline
from book_recommender.pipeline.Recommendation import RecommendationPipeline
import sys

class Main:
    def __init__(self):
        self.training_pipeline = TrainingPipeline()
        self.recommendation_pipeline = RecommendationPipeline()

    def start_training(self):
        try:
            self.training_pipeline.run()
        except Exception as e:
            raise BookRecommenderException(e, sys) from e  # type:ignore

    def get_recommendations(self, book_name):
        try:
            return self.recommendation_pipeline.recommend_books(book_name)
        except Exception as e:
            raise BookRecommenderException(e, sys) from e  # type:ignore
        
if __name__ == "__main__":
    main_app = Main()
    # Start the training pipeline
    # main_app.start_training()
    
    # Example: Get recommendations for a specific book
    book_name = input("Enter a book name: ")  # Replace with an actual book name from your dataset
    recommendations = main_app.get_recommendations(book_name)
    print(f"Recommendations for '{book_name}':")
    for book, poster in zip(recommendations["recommended_books"], recommendations["poster_urls"]):
        print(f"Book: {book}")
        print(f"Poster: {poster}")
        print("---")
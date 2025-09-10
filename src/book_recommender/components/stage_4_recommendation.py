import os
import sys
import pickle
from book_recommender.config.configuration import WebAppConfiguration
from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger

class RecommendationEngine:
    def __init__(self, config=WebAppConfiguration()):
        try:
            self.config = config.get_recommendation_config()
        except Exception as e:
            raise BookRecommenderException(e, sys) from e  # type:ignore
        
    def extract_book_names(self):
        try:
            book_names_path = self.config.book_name_serialized_file
            if not os.path.exists(book_names_path):
                raise FileNotFoundError(f"Book names file not found at {book_names_path}")
            with open(book_names_path, 'rb') as file:
                book_names = pickle.load(file)
            logger.info(f"Extracted {len(book_names)} book names.")
            return book_names
        except Exception as e:
            raise BookRecommenderException(e, sys) from e  # type:ignore

    def recommend_books(self, book_name):
        try:
            # Load the trained model
            model_path = self.config.trained_model_path
            model = pickle.load(open(model_path, 'rb'))
            logger.info(f"Loaded model from {model_path}")

            # Load the transformed data
            book_pivot = pickle.load(open(self.config.book_pivot_serialized_file, 'rb'))
            final_rating = pickle.load(open(self.config.final_rating_serialized_file,'rb'))

            logger.info("Loaded transformed data for recommendations.")

            # Get the user vector
            user_vector = book_pivot.loc[book_name,:].values.reshape(1, -1)

            # Get recommendations
            _, indices = model.kneighbors(user_vector, n_neighbors=self.config.num_recommendations)
            recommended_books = book_pivot.index[indices.flatten()].tolist()
            poster_urls = []
            for book in recommended_books:
                poster_url = final_rating.loc[final_rating["Title"] == book, "ImageURL"].values[0]
                poster_urls.append(poster_url)
            logger.info(f"Recommended books for {book_name}")
            recommendation = {
                "recommended_books": recommended_books,
                "poster_urls": poster_urls
            }
            return recommendation

        except Exception as e:
            raise BookRecommenderException(e, sys) from e  # type:ignore
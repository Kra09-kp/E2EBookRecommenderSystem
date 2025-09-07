import os
import sys
import pickle   
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from book_recommender.config.configuration import WebAppConfiguration
from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger

class ModelTrainer:
    def __init__(self, config = WebAppConfiguration()):
        try:
            self.config = config.get_model_training_config()
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore

    def train_model(self):
        try:
            # Load the transformed data
            book_pivot = pickle.load(open(self.config.transformed_data_file_path, 'rb'))

            # Convert to sparse matrix
            book_pivot_matrix = csr_matrix(book_pivot.values)
            logger.info("Converted book pivot table to sparse matrix.")

            # Initialize and train the model
            logger.info("Training the model...")
            model = NearestNeighbors(algorithm='brute') 
            model.fit(book_pivot_matrix)
            logger.info("Model training completed.")

            # Save the trained model
            os.makedirs(self.config.trained_model_dir, exist_ok=True)
            pickle.dump(model, open(os.path.join(self.config.trained_model_dir, self.config.trained_model_name), 'wb'))
            
            logger.info(f"Trained model saved at {os.path.join(self.config.trained_model_dir, self.config.trained_model_name)}")

        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore

    def initiate_model_training(self):
        try:
            logger.info("--> Starting model training")
            self.train_model()
            logger.info("--> Model training completed")
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore
        


if __name__ == "__main__":
    try:
        obj = ModelTrainer()
        obj.initiate_model_training()
    except Exception as e:
        raise BookRecommenderException(e, sys) from e #type:ignore
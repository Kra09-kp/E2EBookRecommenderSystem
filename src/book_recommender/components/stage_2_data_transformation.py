import os
import sys
import pickle
import pandas as pd
from book_recommender.config.configuration import WebAppConfiguration
from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.logger.log import logger


class DataTransformation:
    def __init__(self, config = WebAppConfiguration()):
        try:
            self.data_transform_config = config.get_data_transformation_config()
            self.data_validation_config = config.get_data_validation_config()
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore

    def do_data_transformation(self):
        try:
            df = pd.read_csv(os.path.join(self.data_transform_config.clean_data_file_path))

            # lets create pivot table
            book_pivot = df.pivot_table(index='Title', columns='UserID', values='BookRating', fill_value=0)
            logger.info("Shape of book pivot table: {}".format(book_pivot.shape))

            # saving the pivot table
            os.makedirs(self.data_transform_config.transformed_data_dir, exist_ok=True)
            pickle.dump(book_pivot, open(os.path.join(self.data_transform_config.transformed_data_dir,'book_pivot.pkl'), 'wb'))
            logger.info("Book pivot table saved successfully.")

            book_names = book_pivot.index

            # saving book name for the web app
            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(book_names, open(os.path.join(self.data_validation_config.serialized_object_dir,'book_names.pkl'), 'wb'))
            logger.info("Book names saved successfully.")

            # saving book pivot for the webapp
            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(book_pivot, open(os.path.join(self.data_validation_config.serialized_object_dir,'book_pivot.pkl'), 'wb'))
            logger.info("Book pivot saved successfully.")
            
            
 
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore
    
    def initiate_data_transformation(self):
        try:
            logger.info("--> Starting data transformation")
            self.do_data_transformation()
            logger.info("--> Data transformation completed")
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore
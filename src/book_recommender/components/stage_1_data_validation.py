import os 
import sys
import pandas as pd
import pickle
from book_recommender.logger.log import logger
from book_recommender.exception.exception_handler import BookRecommenderException
from book_recommender.config.configuration import WebAppConfiguration

class DataValidation:
    def __init__(self, config = WebAppConfiguration()):
        """
            Data Validation Component
        """
        try:
            logger.info(f"{'>>'*20} Data Validation log started {'<<'*20}")
            self.config = config.get_data_validation_config()
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore
    
    def validate_data(self):
        try:
            books = pd.read_csv(self.config.books_file,low_memory=False)
            ratings = pd.read_csv(self.config.ratings_file,low_memory=False)

            logger.info(f"Books data shape: {books.shape}")
            logger.info(f"Ratings data shape: {ratings.shape}")

            books = books[["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher", "Image-URL-L"]]
            books.rename(columns={
                            "Book-Title": "Title",
                            "Book-Author": "Author",
                            "Year-Of-Publication": "Year",
                            "Publisher": "Publisher",
                            "Image-URL-L": "ImageURL"
                        }, inplace=True)
            ratings.rename(columns=
               {"User-ID": "UserID",
               "Book-Rating": "BookRating"}, inplace=True)
            logger.info("Renamed columns in books and ratings data")

            #lets have only those users who have rated atleast 50 books
            ratings = ratings.groupby("UserID").filter(lambda x: len(x) > 50)

            # Merge books and ratings data to get the number of ratings per book
            books_with_ratings = books.merge(ratings, on="ISBN")
            number_ratings = books_with_ratings.groupby('Title')['BookRating'].count().reset_index()
            number_ratings.rename(columns={
                    "BookRating": "TotalRatingCount"
                }, inplace=True)
            final_rating = books_with_ratings.merge(number_ratings, on='Title')
            final_rating = final_rating[final_rating["TotalRatingCount"] >= 50]
            final_rating = final_rating.drop_duplicates(['UserID', 'Title'])
            logger.info(f"Final data shape after filtering users with at least 50 ratings: {final_rating.shape}")
            
            # saving the final clean data from data transformation
            os.makedirs(self.config.clean_data_dir, exist_ok=True)
            final_rating.to_csv(self.config.clean_data_dir / "clean_data.csv", index=False)
            logger.info(f"Final rating data saved at {self.config.clean_data_dir / 'clean_data.csv'}")

            # saving final_rating object for web application
            os.makedirs(self.config.serialized_object_dir, exist_ok=True)
            pickle.dump(final_rating, open(self.config.serialized_object_dir / 'final_rating.pkl', 'wb'))
            logger.info(f"Final rating data object saved at {self.config.serialized_object_dir / 'final_rating.pkl'}")


        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore
        
    
    def initiate_data_validation(self):
        try:
            logger.info("--> Starting data validation")
            self.validate_data()
            logger.info("--> Data validation completed")
        except Exception as e:
            raise BookRecommenderException(e, sys) from e #type:ignore
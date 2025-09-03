from book_recommender.exception.exception_handler import WebAppException
from book_recommender.logger.log import logger
import sys

def main():

    logger.info("Hello from e2ebookrecommendersystem!")

    try:
        a = 3/0

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise WebAppException(e, sys) from e #type: ignore
        # print(e) 


if __name__ == "__main__":
    main()

from fastapi import APIRouter
from book_recommender.exception.exception_handler import BookRecommenderException
import sys
from book_recommender.logger.log import logger
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import pickle
from book_recommender.pipeline.Recommendation import RecommendationEngine

router = APIRouter()
recommendation_engine = RecommendationEngine()

@router.get("/books")
async def get_book_names():
    try:
        book_names = recommendation_engine.extract_book_names()
        # print(book_names.values)
        return JSONResponse(content={"books": book_names.values.tolist()})  
    except Exception as e:
        raise BookRecommenderException(e, sys) from e  # type:ignore
from fastapi import APIRouter
from book_recommender.pipeline.Training import TrainingPipeline
from book_recommender.exception.exception_handler import BookRecommenderException
import sys
from book_recommender.logger.log import logger
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")

router = APIRouter()
training_pipeline = TrainingPipeline()

@router.post("/train")
async def train_model():
    try:
        logger.info("Starting the training pipeline")
        training_pipeline.run()
        return JSONResponse(content={"message": "Training completed successfully"})
    except Exception as e:
        raise BookRecommenderException(e, sys) from e  # type:ignore
    
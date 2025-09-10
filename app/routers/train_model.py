from fastapi import APIRouter
from book_recommender.pipeline.Training import TrainingPipeline
from book_recommender.logger.log import logger
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse


templates = Jinja2Templates(directory="app/templates")
steps = [
    "Data Ingestion",
    "Data Validation",
    "Data Transformation",
    "Model Training"
]

router = APIRouter()
training_pipeline = TrainingPipeline(steps)

@router.get("/train-stream")
async def train_model():
    try:
        logger.info("Training Started")
        return StreamingResponse(
        training_pipeline.run(),  # generator with yield
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache","Connection": "keep-alive"},
        status_code=200
    )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong")

from fastapi import APIRouter
from book_recommender.pipeline.Recommendation import RecommendationPipeline
from book_recommender.logger.log import logger
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException



templates = Jinja2Templates(directory="app/templates")

router = APIRouter()
recommendation_pipeline = RecommendationPipeline()


@router.get("/recommend/", response_class=JSONResponse)
async def recommend_books(book: str):
    try:
        logger.info(f"Getting recommendations for book: {book}")
        recs = recommendation_pipeline.recommend_books(book)

        # recs expected: {"recommended_books": [...], "poster_urls": [...]}
        books = recs.get("recommended_books", [])
        posters = recs.get("poster_urls", [])

        result = [
            {"title": b, "poster": p}
            for b, p in zip(books[1:], posters[1:])
        ]

        return JSONResponse(content={"recommendations": result})

    except Exception as e:
        raise HTTPException(status_code=500,detail="Something went wrong")

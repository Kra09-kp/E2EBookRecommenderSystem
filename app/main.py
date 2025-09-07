from fastapi import FastAPI,Request,APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from book_recommender.logger.log import logger
from book_recommender.exception.exception_handler import BookRecommenderException
import sys
from app.routers import train_model,book_recommend,book_names
from fastapi.middleware.cors import CORSMiddleware
import os

def delete_temp_files_and_folders(temp_dir="temp"):
    if os.path.exists(temp_dir):
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(temp_dir)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting the Book Recommendation API")
    yield
    try:
        # delete_temp_files_and_folders("artifacts")
        pass
    except Exception as e:
        logger.error(f"Error cleaning up temporary files and folders: {str(e)}")
    logger.info("Book Recommendation API has ended properly")

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="./app/templates")

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )


app.mount("/static", StaticFiles(directory="./app/templates/static", html=True), name="static")
app.include_router(train_model.router)
app.include_router(book_names.router)
app.include_router(book_recommend.router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
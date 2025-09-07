from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    dataset_url: str
    raw_data_dir: Path
    ingested_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    clean_data_dir: Path
    serialized_object_dir: Path
    books_file: str
    ratings_file: str


@dataclass(frozen=True)
class DataTransformationConfig:
    transformed_data_dir: Path
    clean_data_file_path: Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    transformed_data_file_path:Path
    trained_model_dir: Path
    trained_model_name: str

@dataclass(frozen=True)
class RecommendationConfig:
    book_pivot_serialized_file: Path
    final_rating_serialized_file: Path
    book_name_serialized_file: Path
    trained_model_path: Path
    trained_model_name: str
    num_recommendations: int
import setuptools


SRC_REPO="BookRecommendationSystem"
AUTHOR_USER_NAME = "Kra09-kp"
AUTHOR_EMAIL="kirtipogra@gmail.com"
REPO_NAME="E2EBookRecommenderSystem"
__version__ = "0.1.0"

with open("readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small package for Book Recommendation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir = {"": "src"},
    packages=setuptools.find_packages(where="src"),   
)
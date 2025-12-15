from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def root():
    return {"message": "Welcom to our Samart Document Management",
            "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

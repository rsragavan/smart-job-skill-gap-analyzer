from fastapi import FastAPI

app = FastAPI(
    title="Smart Job Skill Gap Analyzer",
    version="1.0.0",
    description="Backend API for scraping Greenhouse jobs and analyzing skill gaps."
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Smart Job Skill Gap Analyzer API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
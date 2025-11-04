# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.resume_routes import router as resume_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Resume Analyser API",
    version="1.0.0",
    description="Structured resume parsing powered by Gemini Flash",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (modular)
app.include_router(resume_router, prefix="/api/resumes", tags=["Resumes"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

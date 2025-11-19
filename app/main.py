# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api.routes.resume_routes import router as resume_router
from app.api.routes.feedback_routes import router as feedback_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Resume Analyser API",
    version="1.0.0",
    description="Structured resume parsing powered by Gemini Flash",
)

port = int(os.environ.get("PORT", 8000))

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SECRET_KEY"),
    same_site="none",       # or "none" if frontend runs on another port
    https_only=True,       # must be False during local dev over HTTP
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (modular)
app.include_router(resume_router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

# if __name__ == "__main__":
#     import uvicorn
#     print("Starting server...")
#     uvicorn.run("app.main:app", host="0.0.0.0", port=port)

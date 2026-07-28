from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Workspace",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Enterprise AI Workspace API"
    }
"""
Launcher for SmartKYC FastAPI MVC Server.
"""
import uvicorn

if __name__ == "__main__":
    print("Starting SmartKYC MVC Server on http://localhost:8000...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

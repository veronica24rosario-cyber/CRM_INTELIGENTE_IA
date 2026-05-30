from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from infrastructure.db.database import init_db
from infrastructure.api.router import router

app = FastAPI(title="CRM Inteligente", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=404, content={"detail": "Not Found"})
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.isfile(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend not built"}
else:
    @app.get("/")
    async def root():
        return {
            "message": "CRM Inteligente API",
            "frontend": "Ejecuta 'npm run dev' en /frontend para el frontend de desarrollo",
        }


@app.on_event("startup")
def on_startup():
    init_db()

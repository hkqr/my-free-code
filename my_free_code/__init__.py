from fastapi import FastAPI
from .api.routes import router

app = FastAPI(title="My Free Code", version="0.8.0")
app.include_router(router)

def main():
    import uvicorn
    from .config import settings
    uvicorn.run(app, host=settings.host, port=settings.port)

if __name__ == "__main__":
    main()

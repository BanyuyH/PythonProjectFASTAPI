from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import mongodb
from app.routes import users

# ✅ FIXED: Correct lifespan syntax
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - connect to database
    await mongodb.connect()
    yield
    # Shutdown - disconnect from database
    await mongodb.close()

app = FastAPI(lifespan=lifespan)

# ✅ FIXED: Include router ONLY ONCE with a base prefix
app.include_router(users.router, prefix="/api", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Connection"}

@app.get('/health')
async def health():
    return {"message": "Healthy", "Database": "Connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
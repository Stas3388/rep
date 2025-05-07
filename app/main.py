from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from app.Exception import BaseAppException
from app.routes.auth import router as auth_router
from app.routes.category import router as category_router
from app.routes.transaction import router as transaction_router
from contextlib import asynccontextmanager
from app.core.database import create_tables, engine


@asynccontextmanager
async def time_life(app: FastAPI):
    await create_tables()
    yield
    await engine.dispose()  ########xx
    
app = FastAPI(lifespan=time_life)

app.include_router(auth_router)  # В ОДИН ВСЕ НЕЛЬЗЯ ЗАСУНУТЬ(((((((
app.include_router(transaction_router)
app.include_router(category_router)


@app.get("/health", summary="ТЕСТОВАЯ РУЧКА")
def health():
    return {"message":"Hello"}

if __name__ == "__main__": 
    uvicorn.run("app.main:app", reload=True) #?????????
    
@app.exception_handler(BaseAppException)
async def base_app_exception_handler(request: Request, ex: BaseAppException):
    return JSONResponse(status_code=ex.status_code, content={"detail": ex.detail})

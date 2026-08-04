from app.database.database import Base,engine
from fastapi import FastAPI
from app.routers.event_router import event_router
from app.routers.user_router import user_router
from app.routers.reservation_router import res_router

app = FastAPI()

app.include_router(user_router)
app.include_router(event_router)
app.include_router(res_router)
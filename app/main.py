from database.database import Base,engine
from fastapi import FastAPI
from routers.event_router import event_router
from routers.user_router import user_router
from routers.reservation_router import res_router

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(event_router)
app.include_router(res_router)
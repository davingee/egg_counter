from dotenv import load_dotenv  # type: ignore

load_dotenv(override=True)
from shared import helper
from fastapi import FastAPI, Request  # type: ignore
from fastapi.staticfiles import StaticFiles  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from pathlib import Path
from app.clients import db
from app.api.routes import router as api_router
from app.api.websocket import websocket_endpoint
# from app.controller import counter  # your EggCounterController
# from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 🔹 Startup logic
#     print("Starting app")
#     await db.connect()  # or db.init(), or whatever your startup requires

#     yield  # 🔹 App is running

#     # 🔹 Shutdown logic
#     print("Shutting down app")
#     counter.stop()
#     await db.disconnect()  # you have a disconnect or close

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.add_api_websocket_route("/ws/house_counts", websocket_endpoint)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

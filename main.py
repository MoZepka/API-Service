from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Клуб будущего")
templates = Jinja2Templates(directory="templates")

EVENTS = [
  {
    "id": 1,
    "title": "Artemis II: Облет Луны",
    "seats": 8,
    "status": "Регистрация"
  },
  {
    "id": 2,
    "title": "ExoMars: Поиск жизни",
    "seats": 2,
    "status": "Выполнение"
  },
  {
    "id": 3,
    "title": "SpaceX Crew-9",
    "seats": 4,
    "status": "Завершен"
  }
]

class Event(BaseModel):
    id: int
    title: str
    seats: int
    status: str

@app.get("/", response_class=HTMLResponse)
def index_GET(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"events": EVENTS})

@app.get("/api/events", response_model=list[Event])
def events_GET():
    return EVENTS


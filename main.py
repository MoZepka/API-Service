from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Клуб будущего")
templates = Jinja2Templates(directory="templates")

EVENTS = [
  {
    "id": 1,
    "direction": "Космическая миссия",
    "title": "Artemis II: Облет Луны",
    "seats": 8,
    "status": "Регистрация"
  },
  {
    "id": 2,
    "direction": "Дистанционное управление",
    "title": "ExoMars: Поиск жизни",
    "seats": 2,
    "status": "Выполнение"
  },
  {
    "id": 3,
    "direction": "Космическая миссия",
    "title": "SpaceX: Crew-9",
    "seats": 0,
    "status": "Завершен"
  }
]

class Event(BaseModel):
    id: int
    direction: str
    title: str
    seats: int
    status: str

@app.get("/", response_class=HTMLResponse)
def index_GET(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"events": EVENTS})

@app.get("/api/events", response_model=list[Event])
def events_GET():
    return EVENTS

@app.get("/api/events/open", response_model=list[Event])
def open_GET():
    return [event for event in EVENTS if event['status'] == "Регистрация"]
        


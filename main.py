from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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

class EventCreate(BaseModel):
    direction: str
    title: str
    seats: int

@app.get("/", response_class=HTMLResponse)
def index_GET(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"events": EVENTS})

@app.get("/events/new", response_class=HTMLResponse)
def form_GET(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")

@app.post("/events/new")
def form_POST(title: str = Form(), seats: int = Form(), direction: str = Form()):
    new_event = {"id": len(EVENTS) + 1,
                 "direstion": direction,
                 "title": title,
                 "seats": seats,
                 "status": "Регистрация"}
    if seats == 0:
        new_event["status"] = "Выполнение"
    EVENTS.append(new_event)
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/events")
def events_GET():
    return EVENTS

@app.post("/api/events", response_model=EventCreate, status_code=201)
def events_POST(event: EventCreate):
    new_event = event.model_dump()
    new_event["id"] = len(EVENTS) + 1
    if new_event["seats"] == 0:
        new_event["status"] = "Выполнение"
    else:
        new_event["status"] = "Регистрация"
    EVENTS.append(new_event)
    return new_event

@app.get("/api/events/open", response_model=list[Event])
def open_GET():
    return [event for event in EVENTS if event['status'] == "Регистрация"]
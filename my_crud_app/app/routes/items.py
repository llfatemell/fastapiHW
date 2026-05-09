from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
DATA_FILE = "items.json"

def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@router.get("/landing", response_class=HTMLResponse)
async def landing_page(request: Request):
    items = load_items()
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={"items": items}
    )
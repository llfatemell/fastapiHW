from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.items import router as items_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(items_router)

@app.get("/")
async def landing(request: Request):
    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request
        }
    )

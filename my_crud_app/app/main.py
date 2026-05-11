from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import items

app = FastAPI(title="Items CRUD - Step by Step")
app.include_router(items.api_router)

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include the items router (all routes under /items)
app.include_router(items.router, prefix="/items")

@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/items/landing")
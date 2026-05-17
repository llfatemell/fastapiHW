from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
from pathlib import Path

router = APIRouter(prefix="/items", tags=["items"])
templates = Jinja2Templates(directory="app/templates")

DATA_FILE = Path("app/data/items.json")


def load_items():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_items(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=2)


@router.get("/")
async def list_items(request: Request):
    items = load_items()
    return templates.TemplateResponse("items_list.html", {
        "request": request,
        "items": items
    })


@router.get("/new")
async def new_item_form(request: Request):
    return templates.TemplateResponse("item_form.html", {
        "request": request,
        "editing": False
    })


@router.post("/")
async def create_item(
    name: str = Form(...),
    price: float = Form(...),
    is_offer: bool = Form(False)
):
    items = load_items()

    # Generate new ID
    new_id = max([item["id"] for item in items], default=-1) + 1

    # Create new item
    new_item = {
        "id": new_id,
        "name": name,
        "price": price,
        "is_offer": is_offer
    }

    items.append(new_item)
    save_items(items)

    return RedirectResponse(url="/items/", status_code=303)


@router.get("/edit/{item_id}")
async def edit_item_form(request: Request, item_id: int):
    items = load_items()

    # Find item by ID
    item = next((item for item in items if item["id"] == item_id), None)

    if not item:
        return RedirectResponse(url="/items/", status_code=303)

    return templates.TemplateResponse("item_form.html", {
        "request": request,
        "editing": True,
        "item_id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "is_offer": item["is_offer"]
    })


@router.post("/{item_id}")
async def update_item(
    item_id: int,
    name: str = Form(...),
    price: float = Form(...),
    is_offer: bool = Form(False)
):
    items = load_items()

    # Find item index
    item_index = next((i for i, item in enumerate(items) if item["id"] == item_id), None)

    if item_index is None:
        return RedirectResponse(url="/items/", status_code=303)

    # Update item
    items[item_index] = {
        "id": item_id,
        "name": name,
        "price": price,
        "is_offer": is_offer
    }

    save_items(items)

    return RedirectResponse(url="/items/", status_code=303)


@router.post("/delete/{item_id}")
async def delete_item(item_id: int):
    items = load_items()

    # Remove item with matching ID
    items = [item for item in items if item["id"] != item_id]

    save_items(items)

    return RedirectResponse(url="/items/", status_code=303)

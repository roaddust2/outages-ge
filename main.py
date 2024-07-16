import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import List

from app.parser.gwp import GWP


# Configure basic logger

logging.basicConfig(level=logging.INFO)


# Define the app and add static with jinja2 templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Handlers

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page handler"""

    return templates.TemplateResponse(request, "index.html")


@app.get("/outages", response_model=List[dict])
async def outages():
    """Outages"""

    gwp_provider = GWP()
    outages = []
    try:
        gwp_outages = await gwp_provider.get_outages()
        outages.extend(gwp_outages)
    except GetOutagesError as err:
        logging.error(f"Error occured while getting outages:\n{err}")
    return outages

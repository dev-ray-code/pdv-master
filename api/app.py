from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database.db import criar_banco
from api.licencas import router as licencas_router

app = FastAPI(
    title="PDV Store Server",
    version="1.0"
)

app.include_router(licencas_router)

templates = Jinja2Templates(directory="api/templates")

app.mount("/static", StaticFiles(directory="api/static"), name="static")


@app.on_event("startup")
def startup():
    criar_banco()


@app.get("/")
def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )


@app.get("/clientes")
def clientes(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="clientes.html",
        context={"request": request}
    )


@app.get("/licencas")
def licencas(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="licencas.html",
        context={"request": request}
    )
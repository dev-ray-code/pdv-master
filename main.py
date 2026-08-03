from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database.db import criar_banco

from api.licencas import router as licencas_router

from api.clientes import router as clientes_router
from api.dispositivos import router as dispositivos_router
from api.dashboard import router as dashboard_router
from api.mobile import router as mobile_router
from api.windows import router as windows_router
from api.auth import router as auth_router
from api.usuarios import router as usuarios_router

app = FastAPI(
    title="PDV Store Server",
    version="1.0"
)

app.include_router(licencas_router)
app.include_router(clientes_router)
app.include_router(dispositivos_router)
app.include_router(dashboard_router)
app.include_router(mobile_router)
app.include_router(windows_router)
app.include_router(auth_router)
app.include_router(usuarios_router)

templates = Jinja2Templates(directory="api/templates")

app.mount("/static", StaticFiles(directory="api/static"), name="static")


@app.on_event("startup")
def startup():
    criar_banco()

from fastapi.responses import PlainTextResponse

@app.exception_handler(Exception)
async def erro_global(request, exc):
    import traceback

    print("========== ERRO ==========")
    traceback.print_exc()

    return PlainTextResponse(
        "Erro interno",
        status_code=500
    )

@app.get("/")
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
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
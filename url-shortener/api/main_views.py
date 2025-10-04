from datetime import date, datetime

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from templating.jinja_templates import templates

router = APIRouter()


@router.get("/home/", response_class=HTMLResponse, include_in_schema=False, name="home")
def home_page(
    request: Request,
) -> HTMLResponse:
    # features = ["Short link generation", "Contact the author", "Paid plan"]
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        # context={"features": features},
    )


@router.get(
    "/about/", response_class=HTMLResponse, include_in_schema=False, name="about"
)
def about_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )


@router.get("/")
def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="init.html")

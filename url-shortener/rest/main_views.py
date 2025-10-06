from typing import Any

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from templating.jinja_templates import templates

router = APIRouter()


@router.get("/", name="initial", include_in_schema=False)
def init_page(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    features = [
        "Create short URLs",
        "Track all redirects",
        "Real-time statistics",
        "Shared management",
    ]
    return templates.TemplateResponse(
        request=request,
        name="base.html",
        context={"features": features},
    )


@router.get("/home", response_class=HTMLResponse, name="home")
def home_page(
    request: Request,
) -> HTMLResponse:
    features = ["Short link generation", "Contact the author", "Paid plan"]
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"features": features},
    )


@router.get("/about/", response_class=HTMLResponse, name="about")
def about_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )

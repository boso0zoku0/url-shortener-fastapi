from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, Request
from pydantic import BaseModel, ValidationError
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.short_urls import GetShortUrlsStorage
from schemas import ShortUrlCreate
from services.short_urls.form_response_helper import FormResponseHelper
from storage.short_urls.exceptions import ShortUrlAlreadyExists
from templating import templates

router = APIRouter(prefix="/create")

form_helper = FormResponseHelper(
    model_schema=ShortUrlCreate, template_name="films/create.html"
)


@router.get("/", name="short-urls:create_views")
def get_page_create_short_url(request: Request) -> HTMLResponse:
    return form_helper.render(request=request)


@router.post("/", name="short-urls:create", response_model=None)
async def create_short_url(
    request: Request,
    storage: GetShortUrlsStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            short_url_create = ShortUrlCreate.model_validate(form)

        except ValidationError as e:
            return form_helper.render(
                request=request,
                pydantic_error=e,
                form_data=form,
                form_validated=True,
            )

    try:
        storage.create_or_raise_if_exists(short_url_create)

    except ShortUrlAlreadyExists:
        errors = {
            "slug": f"Short url with slug {short_url_create.slug!r} already exists."
        }

    else:
        return RedirectResponse(
            url=request.url_for("short-urls:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return form_helper.render(
        request=request, errors=errors, form_validated=True, form_data=short_url_create
    )

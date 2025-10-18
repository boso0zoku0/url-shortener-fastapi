from collections.abc import Mapping
from typing import Annotated, Any

from fastapi import APIRouter, Form, Request
from pydantic import BaseModel, ValidationError
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.short_urls import GetShortUrlsStorage
from schemas import ShortUrlCreate
from storage.short_urls.exceptions import ShortUrlAlreadyExists
from templating import templates

router = APIRouter(prefix="/create")


@router.get("/", name="short-urls:create_views")
def get_page_create_short_url(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = ShortUrlCreate.model_json_schema()
    context.update(model_schema=model_schema)
    return templates.TemplateResponse(
        request=request,
        name="short-urls/create.html",
        context=context,
    )


def create_view_validation_response(
    request: Request,
    errors: dict[str, str] | None = None,
    form_data: BaseModel | Mapping[str, Any] | None = None,
    *,
    form_validated: bool = True,
) -> HTMLResponse:
    model_schema = ShortUrlCreate.model_json_schema()
    context: dict[str, Any] = {}
    context.update(
        errors=errors,
        model_schema=model_schema,
        form_validated=form_validated,
        form_data=form_data,
    ),

    return templates.TemplateResponse(
        request=request,
        name="short-urls/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def parse_pydantic_error(error: ValidationError) -> dict[str, str]:
    return {f"{err['loc'][0]}": err["msg"] for err in error.errors()}


@router.post("/", name="short-urls:create", response_model=None)
async def create_short_url(
    request: Request,
    storage: GetShortUrlsStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            short_url_create = ShortUrlCreate.model_validate(form)
        except ValidationError as e:
            errors = parse_pydantic_error(e)
            return create_view_validation_response(
                request=request,
                errors=errors,
                form_data=form,
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

    return create_view_validation_response(
        request=request,
        errors=errors,
        form_data=short_url_create,
    )

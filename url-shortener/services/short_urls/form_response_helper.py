from typing import Any, Mapping

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError
from starlette import status
from starlette.requests import Request
from starlette.templating import _TemplateResponse

from schemas import ShortUrlCreate
from templating import templates


class FormResponseHelper:
    def __init__(
        self,
        template_name: str,
        model_schema: type[BaseModel],
    ) -> None:
        self.template_name = template_name
        self.model_schema = model_schema

    def parse_pydantic_error(self, error: ValidationError) -> dict[str, str]:
        return {f"{err['loc'][0]}": err["msg"] for err in error.errors()}

    def render(
        self,
        request: Request,
        errors: dict[str, str] | None = None,
        pydantic_error: ValidationError | None = None,
        *,
        form_validated: bool = False,
        form_data: BaseModel | Mapping[str, Any] | None = None,
    ) -> _TemplateResponse:
        model_schema = ShortUrlCreate.model_json_schema()
        context: dict[str, Any] = {}
        if pydantic_error:
            errors = self.parse_pydantic_error(error=pydantic_error)

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
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
                if form_validated and errors
                else status.HTTP_200_OK
            ),
        )

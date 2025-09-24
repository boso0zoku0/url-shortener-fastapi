from datetime import date, datetime

from fastapi.templating import Jinja2Templates
from fastapi import Request

from core.config import BASE_DIR


def show_dt(request: Request) -> dict[str, date]:
    return {"today": date.today(), "now": datetime.now()}


templates = Jinja2Templates(
    directory=BASE_DIR / "templates", context_processors=[show_dt]
)

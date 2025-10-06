from datetime import date, datetime, timezone

from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR


def show_dt(request: Request) -> dict[str, date]:
    now = datetime.now(timezone.utc)
    today = now.today()
    return {
        "now": now,
        "today": today,
    }


templates = Jinja2Templates(
    directory=BASE_DIR / "templates", context_processors=[show_dt]
)

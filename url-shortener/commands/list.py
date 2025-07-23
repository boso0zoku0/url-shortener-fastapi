from typing import Annotated

import typer
from rich import print

from api.api_v1.auth.services.redis_tokens_helper import db_redis_tokens

list_tokens = db_redis_tokens.get_all_tokens()

app = typer.Typer(
    name="list",
    no_args_is_help=True,
    help="Tokens management.",
    rich_markup_mode="rich",
)


@app.command()
def check():
    print(f"Tokens: [bold]{list_tokens}[/bold]")

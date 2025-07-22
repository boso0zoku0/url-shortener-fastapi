from typing import Annotated

import typer
from rich import print

from api.api_v1.auth.services.redis_tokens_helper import db_redis_tokens

app = typer.Typer(
    name="token",
    help="Tokens management.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def check(token: Annotated[str, typer.Argument(help="The token to check")]):
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exists[/bold green]."
            if db_redis_tokens.token_exists(token)
            else "[bold red]does not exist[/bold red]."
        ),
    )

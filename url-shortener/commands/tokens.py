__app__ = "app"

from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services.redis_tokens_helper import db_redis_tokens

app = typer.Typer(
    name="tokens",
    help="Tokens management.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def check(token: Annotated[str, typer.Argument(help="The token to check")]) -> None:
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exists[/bold green]."
            if db_redis_tokens.token_exists(token)
            else "[bold red]does not exist[/bold red]."
        ),
    )


@app.command(name="list")
def list_check() -> None:
    print(Markdown("# Available API tokens"))
    print((Markdown("\n- ".join([""] + db_redis_tokens.get_all_tokens()))))
    print()


@app.command(name="del")
def delete_token(
    token: Annotated[str, typer.Argument(help="The token to delete")],
) -> None:
    if db_redis_tokens.token_exists(token):
        db_redis_tokens.delete_token(token)
        print(f"[green]Token: {token.center(10)}Successfully deleted[/green]")

    else:
        print()
        print(f"[red]Invalid token: {token}[/red]".center(10))
        print()


@app.command(name="generate")
def generate_token() -> None:
    token = db_redis_tokens.generate_and_save_token()
    print(
        f"[green]Token [violet]{token}[/violet] was successfully created and saved in the database.[/green]"
    )


@app.command(name="add")
def add_token(token: Annotated[str, typer.Argument(help="The token to add")]) -> None:
    if not db_redis_tokens.token_exists(token):
        db_redis_tokens.add_token(token)
        print("[green]Token added[/green]")
        return
    # else:
    print("[red]Error[/red]")

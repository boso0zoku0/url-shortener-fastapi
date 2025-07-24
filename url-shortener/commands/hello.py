__app__ = "app"

from typing import Annotated

import typer
from rich import print

app = typer.Typer(
    name="Greeting",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Greeting command",
)


@app.command()
def hello(greet: Annotated[str, typer.Argument(help="Name to greet")]) -> None:
    print(f"[bolt]Hello[/bolt], [green]{greet}[/green]")

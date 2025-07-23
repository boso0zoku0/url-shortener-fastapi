import typer

from rich import print
from typing import Annotated

app = typer.Typer(
    name="Greeting",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Greeting command",
)


@app.command()
def hello(str: Annotated[str, typer.Argument(help="Name to greet")]):
    print(f"[bolt]Hello[/bolt], [green]{str}[/green]")

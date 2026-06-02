from enum import Enum
from pathlib import Path
from util.ai import create_problem, review_solution
import typer
from rich.console import Console
from rich.panel import Panel
from util.util import open_in_vscode

app = typer.Typer(help="Practice algorithms with AI-generated problems and reviews.")
console = Console()

DEFAULT_FILE = Path("problem.txt")


@app.callback(invoke_without_command=True)
def welcome(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is not None:
        return
    console.print(
        Panel.fit(
            "\n"
            "[bold cyan]Terminal Algo[/bold cyan]\n"
            "[dim]Practice algorithms with AI-generated problems and AI reviews.[/dim]\n"
            "\n"
            "[bold]Commands[/bold]\n"
            "  [green]train[/green] [topic]     Generate a practice problem (opens in VS Code)\n"
            "  [green]review[/green] [file]    Review your solution in a problem file\n"
            "\n"
            "[bold]Examples[/bold]\n"
            "  [dim]main.py[/dim] train recursion\n"
            "  [dim]main.py[/dim] train --custom \"two pointers\"\n"
            "  [dim]main.py[/dim] review\n"
            "  [dim]main.py[/dim] review problem.txt\n"
            "\n"
            "[dim]Tip: run[/dim] [bold]main.py --help[/bold] [dim]for all options.[/dim]\n",
            border_style="cyan",
            title="[bold]Welcome[/bold]",
        )
    )
    raise typer.Exit()


class Topic(str, Enum):
    recursion = "recursion"
    linear_search = "linear search"
    binary_search = "binary search"
    bubble_sort = "bubble sort"


@app.command()
def train(
    topic: Topic | None = typer.Argument(
        None,
        help="Algorithm topic (e.g. recursion, linear_search).",
    ),
    custom: str | None = typer.Option(None, "--custom", "-c", help="Custom topic text."),
    output: Path = typer.Option(DEFAULT_FILE, "--output", "-o", help="Where to write the problem."),
    no_open: bool = typer.Option(False, "--no-open", help="Don't open the file in VS Code after generating."),
) -> None:
    """Generate a new practice problem."""
    name = custom or (topic.value if topic else None)
    if not name:
        console.print("\n[bold]Some Examples could be:[/bold]\n")
        for t in Topic:
            console.print(f"  {t.value}")
        name = typer.prompt("Enter the topic")

    with console.status(f"[bold green]Generating problem for {name}…"):
        create_problem(name, output)

    console.print(f"\n[green]✓[/green] Saved to [bold]{output}[/bold]\n")
    if not no_open:
        open_in_vscode(output)


@app.command()
def review(
    file: Path = typer.Argument(DEFAULT_FILE, help="Problem file with your solution."),
) -> None:
    """Review your solution with AI."""
    if not file.is_file():
        console.print(f"[red]File not found:[/red] {file}")
        raise typer.Exit(1)

    with console.status("[bold green]Reviewing solution…"):
        result = review_solution(file)

    console.print(f"\n[bold green]Review[/bold green]\n{result}\n")


if __name__ == "__main__":
    app()

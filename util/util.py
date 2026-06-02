import os
from pathlib import Path
import shutil
import subprocess
from rich.console import Console

def open_in_vscode(path: Path) -> None:
    console = Console()
    editor = os.environ.get("EDITOR", "code")
    exe = shutil.which(editor)
    if not exe:
        console.print(f"[yellow]'{editor}' not found on PATH.[/yellow] Install VS Code shell command or open manually: {path}")
        return
    subprocess.run([exe, str(path.resolve())])

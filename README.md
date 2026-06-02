# Terminal Algo

CLI tool to practice algorithms: generate problems with a local LLM, solve them in a structured file, then get an AI review of your solution.

## Project structure

```
Terminal-algo/
├── main.py                 # CLI entry point (Typer commands)
├── problem.txt             # Default output / working file for problems
├── pyproject.toml          # Project metadata and dependencies (uv)
├── util/
│   ├── ai.py               # OpenAI client, problem generation, solution review
│   ├── fileInteraction.py  # Problem file read/write and section parsing
│   ├── format.txt          # Example layout for a problem file
│   └── util.py               # Opens generated files in VS Code (or $EDITOR)
└── README.md
```

## How the pieces connect

| File | Role |
|------|------|
| **main.py** | Defines the Typer app: welcome screen, `train` (generate a problem), `review` (review your solution). Handles topic selection and CLI options. |
| **util/ai.py** | Talks to a local model via LM Studio (`http://localhost:1234/v1`). `create_problem()` asks for structured JSON (problem, hints, test). `review_solution()` reads PROBLEM and SOLUTION sections and returns a short rating + feedback. |
| **util/fileInteraction.py** | Writes problems in a fixed section format (`=== PROBLEM ===`, etc.), formats tests/hints/reviews, and extracts sections for the reviewer. |
| **util/util.py** | After `train`, opens the output file with `code` (VS Code) or whatever is set in `EDITOR`. |
| **util/format.txt** | Reference template showing the four sections every problem file uses. |

## Problem file format

Generated and edited files use four labeled sections:

- `=== PROBLEM ===` — title and description  
- `=== TESTS ===` — sample inputs and expected outputs  
- `=== HINTS ===` — numbered hints  
- `=== SOLUTION ===` — your code (fill this in before running `review`)

See `util/format.txt` for an empty template.

## Commands

Run from the project root (with dependencies installed):

```bash
python main.py              # welcome + command list
python main.py train recursion
python main.py train --custom "two pointers"
python main.py train -o my_problem.txt --no-open
python main.py review
python main.py review problem.txt
```

Built topics (enum in `main.py`): `recursion`, `linear_search`, `binary_search`, `bubble_sort`. Any other topic can be passed via `--custom` / `-c` or the interactive prompt.

## Setup

1. **Python** — requires Python ≥ 3.14 (see `.python-version`).
2. **Dependencies** — install with [uv](https://github.com/astral-sh/uv):

   ```bash
   uv sync
   ```

3. **LM Studio** — run a local server on port `1234` with model `llama-3.2-3b-instruct` (configured in `util/ai.py`).
4. **Editor** — optional: VS Code `code` on PATH, or set `EDITOR` for another editor after `train`.

## Dependencies

From `pyproject.toml`: `openai`, `typer` (and Rich via Typer for terminal UI).

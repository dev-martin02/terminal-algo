def write_format_file(filepath, problem, tests, hints, solution=""):
    if isinstance(hints, list):
        hints = "\n".join(f"{i + 1}. {h}" for i, h in enumerate(hints))
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(
            f"=== PROBLEM ===\n{problem}\n\n"
            f"=== TESTS ===\n{tests}\n\n"
            f"=== HINTS ===\n{hints}\n\n"
            f"=== SOLUTION ===\n{solution}\n"
        )

def format_review(data: dict) -> str:
    lines = [f"Rating: {data['rating']}/10", "", data["good"]]
    for tip in data["improve"]:
        lines.append(f"  - {tip}")
    return "\n".join(lines)

def extract_section(text: str, name: str) -> str:
    marker = f"=== {name} ==="
    start = text.find(marker)
    if start == -1:
        return ""
    start = text.index("\n", start) + 1
    end = text.find("\n=== ", start)
    return text[start : end if end != -1 else None].strip()

def format_test(data: dict) -> str:
    return f"Test 1:\n  input: {data['input']}\n  expected: {data['output']}\n\nTest 2:\n  input: {data['input']}\n  expected: {data['output']}"

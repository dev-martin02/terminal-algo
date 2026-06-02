import json
from pathlib import Path
from openai import OpenAI
from util.fileInteraction import write_format_file ,format_review, format_test, extract_section

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio")


def ai_call(messages, schema=None):

    if schema:
        response = client.chat.completions.create(
            model="llama-3.2-3b-instruct",
            temperature=0.7,
            messages=messages,
            response_format=schema  ,
        )
    else:
        response = client.chat.completions.create(
            model="llama-3.2-3b-instruct",
            temperature=0.7,
            messages=messages,
        )
    return response.choices[0].message.content

def create_problem(algorithm_topic: str, outfile: Path) -> None:    # type: ignore
    PROBLEM_SCHEMA = {
        "type": "json_schema",
        "json_schema": {
            "name": "coding_problem",
            "schema": {
                "type": "object",
                "properties": {
                    "problem": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["name", "description"],
                    },
                    "hints": {"type": "array", "items": {"type": "string"}},
                    "test": {
                        "type": "object",
                        "properties": {
                            "input": {"type": "string"},
                            "output": {"type": "string"},
                        },
                        "required": ["input", "output"],
                    },
                },
                "required": ["problem", "hints", "test"],
            },
        },
    }

    messages = [
        {"role": "system", "content": "You are a helpful assistant that creates coding problems."},
        {"role": "user", "content": f"Create a problem for {algorithm_topic}."},
    ]
    data = json.loads(ai_call(messages, PROBLEM_SCHEMA))
    write_format_file(
        outfile,
        f"{data['problem']['name']}\n\n{data['problem']['description']}",
        format_test(data['test']),
        data['hints'],
    )


def review_solution(filepath: Path) -> str:
    REVIEW_SCHEMA = {
        "type": "json_schema",
        "json_schema": {
            "name": "code_review",
            "schema": {
                "type": "object",
                "properties": {
                    "rating": {"type": "integer", "minimum": 1, "maximum": 10},
                    "good": {"type": "string"},
                    "improve": {
                        "type": "array",
                        "items": {"type": "string"},
                        "maxItems": 2,
                    },
                },
                "required": ["rating", "good", "improve"],
            },
        },
    }
    text = filepath.read_text(encoding="utf-8")
    solution = extract_section(text, "SOLUTION")
    if not solution:
        return "No solution to review. Add your code under === SOLUTION ===."

    messages = [
        {
            "role": "system",
            "content": (
                "Review the student's code. Be brief: one sentence for good, "
                "at most two short bullets for improve. No code, no rewrites. if there is no code, say so and don't invent a solution."
            ),
        },
        {
            "role": "user",
            "content": f"Problem: {extract_section(text, 'PROBLEM')}\nSolution: {solution}",
        },
    ]
    return format_review(json.loads(ai_call(messages, REVIEW_SCHEMA)))
from pathlib import Path


PROMPT_DIR = Path("prompts")


def load_prompt(version: str = "v1") -> str:

    prompt_file = PROMPT_DIR / f"{version}.txt"

    if not prompt_file.exists():
        raise FileNotFoundError(
            f"Prompt version '{version}' not found."
        )

    return prompt_file.read_text(
        encoding="utf-8"
    )
"""
Assembles and returns the CodeAgent used by the app.

Backed by Groq via LiteLLMModel (no Hugging Face billing involved).

Design choices:
- We do NOT pass `prompt_templates` into the CodeAgent constructor.
  Newer smolagents requires the full set of keys if you supply any. We let
  the library use its maintained defaults and override ONLY the system prompt.
- File paths are anchored to __file__ so the app works from any CWD.
- CodeAgent (not ToolCallingAgent) is used because CodeAgent expects the
  model to write Python code, which works reliably with the Qwen models
  on Groq.
- Model: groq/qwen/qwen3.8-27b — confirmed available on this account
  (see list_models.py output) and compatible with CodeAgent.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

from smolagents import (
    CodeAgent,
    LiteLLMModel,
    FinalAnswerTool,
)

from tools.custom_tools import (
    get_current_time_in_timezone,
    my_custom_tool,
    calculator,
    get_weather,
)

# Anchor file paths to the location of THIS file, not the current working
# directory. Makes the script robust no matter where it's launched from.
PROJECT_ROOT = Path(__file__).resolve().parent
PROMPTS_FILE = PROJECT_ROOT / "prompts.yaml"
ENV_FILE = PROJECT_ROOT / ".env"

# Load .env with an explicit path so GROQ_API_KEY is always found.
load_dotenv(dotenv_path=ENV_FILE)


# ---------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------
def load_prompt_templates(path: Path = PROMPTS_FILE) -> dict:
    """Load prompt templates from a YAML file."""
    if not path.exists():
        raise FileNotFoundError(
            f"Missing prompt file: {path}\n"
            f"Create a file named 'prompts.yaml' in {PROJECT_ROOT} "
            f"(watch the .yml vs .yaml extension!)."
        )
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if "system_prompt" not in data:
        raise KeyError(
            f"'system_prompt' key not found in {path}. "
            f"Your prompts.yaml must contain a top-level 'system_prompt:' entry."
        )
    return data


# ---------------------------------------------------------------------
# Model setup (Groq via LiteLLM)
# ---------------------------------------------------------------------
def build_model() -> LiteLLMModel:
    """Create the LLM engine backed by Groq's free API."""
    groq_key = (os.environ.get("GROQ_API_KEY") or "").strip()

    if not groq_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set.\n"
            f"  Looked for:  {ENV_FILE}\n"
            f"  File exists: {ENV_FILE.exists()}\n"
            "\n"
            "Fix:\n"
            "  1. Get a free key at https://console.groq.com/keys\n"
            f"  2. Create/edit {ENV_FILE} and put ONE line in it:\n"
            "        GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx\n"
            "     (no quotes, no spaces around '=', no trailing spaces)\n"
            "  3. Restart: python app.py"
        )

    if groq_key.startswith("gsk_your"):
        raise EnvironmentError(
            "GROQ_API_KEY still contains the PLACEHOLDER from .env.example.\n"
            f"  File: {ENV_FILE}\n"
            f"  Current value starts with: {groq_key[:20]}...\n"
            "\n"
            "Fix: open the file and replace the placeholder with your real\n"
            "key from https://console.groq.com/keys, then restart python app.py."
        )

    return LiteLLMModel(
        model_id="groq/qwen/qwen3.8-27b",  # confirmed available on this account
        api_key=groq_key,
        temperature=0.1,   # recommended for Groq code generation
        max_tokens=2048,
    )


# ---------------------------------------------------------------------
# Agent assembly
# ---------------------------------------------------------------------
def build_agent() -> CodeAgent:
    """Build and return the fully configured CodeAgent."""
    model = build_model()

    agent = CodeAgent(
        model=model,
        tools=[
            FinalAnswerTool(),              # required - lets the agent answer
            get_current_time_in_timezone,   # custom tool
            my_custom_tool,                 # dummy custom tool
            calculator,                     # safe arithmetic tool
            get_weather,                    # real weather lookup
        ],
        max_steps=6,
    )

    # Override ONLY the system prompt; smolagents defaults for planning /
    # managed_agent / final_answer are kept as-is.
    agent.prompt_templates["system_prompt"] = load_prompt_templates()["system_prompt"]

    return agent


# ---------------------------------------------------------------------
# Quick CLI smoke test (`python agent.py`)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    agent = build_agent()
    answer = agent.run("What is the current time in London?")
    print("ANSWER:", answer)
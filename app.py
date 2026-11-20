"""
Entry point for the smolagents project.
Launches a local-only Gradio chat interface backed by the CodeAgent.

Note: share=False is critical - it prevents Gradio from downloading and
running the `frpc` reverse-proxy binary, which triggers antivirus alerts
on Windows even though it is not malicious.
"""

from smolagents import GradioUI
from agent import build_agent


def main() -> None:
    agent = build_agent()
    GradioUI(agent).launch(share=False)


if __name__ == "__main__":
    main()
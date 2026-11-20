# Smolagents Implementation

A Python tool-using AI assistant built with Hugging Face `smolagents`. It uses
a Groq-hosted Qwen model through LiteLLM and provides a local Gradio chat UI.

The agent can answer questions using the language model and its registered
tools: current time by timezone, basic arithmetic, and current weather by city.
It also includes a small example custom tool.

## Run locally

1. Install Python and create/activate a virtual environment.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key
   ```

4. Start the chat interface:

   ```powershell
   python app.py
   ```

   The interface runs locally and is not published as a Gradio share link.

To run the command-line smoke test instead, use `python agent.py`.

## Documentation

See [SYSTEM_DOCUMENTATION.md](./SYSTEM_DOCUMENTATION.md) for the architecture,
request flow, tool descriptions, setup details, and the technologies used to
build this project.

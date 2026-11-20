# System Documentation

## 1. Purpose

This project is a Python conversational AI agent that can use tools to answer
questions requiring current time, simple arithmetic, or current weather. It
provides a local browser-based chat interface and a command-line smoke test.

The agent is built with Hugging Face `smolagents` and uses a Qwen model hosted
by Groq. LiteLLM connects the agent framework to the model API. The project is
an implementation and learning project, rather than a deployed hosted service.

## 2. What the system does

- Accepts natural-language questions in a Gradio chat interface.
- Uses the language model to interpret a task and choose from the tools
  registered with the agent.
- Retrieves current local time for a timezone using `pytz`.
- Calculates arithmetic expressions using a restricted Python abstract syntax
  tree (AST) evaluator.
- Looks up a city and retrieves current weather from Open-Meteo's geocoding
  and forecast APIs.
- Returns the tool output to the model, which produces the final response.

The included `my_custom_tool` is an example of a custom tool; it formats its
arguments in a response and does not perform an external action.

This version does not implement web search, image generation, persistent
conversation memory, or Hugging Face Spaces deployment.

## 3. Architecture and request flow

```text
User
  |
  v
GradioUI (app.py) --------------------------+
  |                                         |
  v                                         |
CodeAgent (agent.py)                        |
  |                                         |
  +--> LiteLLMModel --> Groq Qwen model     |
  |                                         |
  +--> registered tools                    |
        |-- timezone lookup (pytz)           |
        |-- arithmetic AST evaluator         |
        |-- city geocoding + weather (HTTP)  |
        +-- example custom tool              |
  |                                         |
  +<-- tool results / model response <-------+
```

For a chat request, the application builds the agent and starts `GradioUI`.
The agent sends the task to the model along with the tool descriptions. The
model can produce Python code that calls one or more registered tools. The
agent observes each result and continues until it can return a final answer or
reaches its six-step limit. The custom system prompt in `prompts.yaml` describes
this Think–Act–Observe flow; the other prompt templates use `smolagents`
defaults.

`app.py` launches Gradio with `share=False`, so the app stays local rather than
creating a public share link. `agent.py` can also be run directly to execute a
small time-zone smoke-test question.

## 4. Main components

| File | Responsibility |
|---|---|
| `app.py` | Builds the agent and starts the local Gradio chat interface. |
| `agent.py` | Loads configuration and the system prompt, constructs the Groq model, and registers tools with `CodeAgent`. |
| `prompts.yaml` | Defines the system prompt that explains how the agent should use its tools. |
| `tools/custom_tools.py` | Implements the time, example, calculator, and weather tools. |
| `list_models.py` | Optional utility for querying Groq's model-list endpoint using the configured API key. |
| `requirements.txt` | Lists the Python packages used by the project. |
| `.gitignore` | Excludes the local environment, Python caches, and `.env` secrets from Git. |
| `.env` | Local configuration for the Groq API key; create this file yourself and do not commit it. |

### Agent construction

`build_agent()` in `agent.py` performs the following setup:

1. Creates a `LiteLLMModel` configured for `groq/qwen/qwen3.8-27b`, with a
   temperature of `0.1` and a maximum of 2,048 tokens.
2. Registers `FinalAnswerTool` and the four project tools with a `CodeAgent`.
3. Limits each agent run to six steps.
4. Loads the top-level `system_prompt` from `prompts.yaml` and overrides only
   that prompt, leaving the other `smolagents` templates at their defaults.

Paths to `.env` and `prompts.yaml` are based on the directory containing
`agent.py`, so launching the program from another working directory does not
change where those files are searched for.

### Available tools

| Tool | Purpose and implementation |
|---|---|
| `get_current_time_in_timezone(timezone)` | Uses `pytz` to format the current local time in a named timezone. |
| `calculator(expression)` | Parses an arithmetic expression and evaluates only numeric constants and explicitly allowed arithmetic operators. It does not use Python `eval()`. |
| `get_weather(city)` | Finds a city using Open-Meteo geocoding, then requests current temperature, humidity, wind, condition, and local time from Open-Meteo. |
| `my_custom_tool(arg1, arg2)` | Example tool that returns the supplied values in a string. |
| `FinalAnswerTool` | Lets the agent signal that it has completed its response. |

The weather integration makes HTTP requests with a ten-second timeout. The
time, calculator, and weather tools return readable error strings for
tool-level errors, so the agent can incorporate those results into its answer.

## 5. Technologies and tools used to build it

### Application and runtime

- **Python** — application language and tool implementation.
- **Hugging Face `smolagents`** — `CodeAgent`, tool decorator, final-answer
  tool, and Gradio integration.
- **LiteLLM** — adapter used by `smolagents` to call the Groq model.
- **Groq API** — hosted inference for `groq/qwen/qwen3.8-27b`.
- **Gradio** — local browser-based user interface.
- **PyYAML** — loads the system prompt from YAML.
- **python-dotenv** — loads `GROQ_API_KEY` from the local `.env` file.
- **pytz** — timezone database and timezone conversions.
- **Requests** — HTTP calls to Open-Meteo.
- **Open-Meteo APIs** — city geocoding and current weather data.

### Development and project tooling

- **pip** — installs the dependencies listed in `requirements.txt`.
- **Git and GitHub** — version-control and repository workflow, as reflected
  in the project README and repository.
- **Visual Studio Code** — the project development environment.

The runtime packages and minimum versions are declared in `requirements.txt`.
The IDE and version-control tools are development tools, not runtime
dependencies.

## 6. Setup and operation

### Requirements

- Python 3.11 or later.
- A Groq API key.
- Network access for Groq inference and Open-Meteo weather requests.

### Install

From the project directory, create and activate a virtual environment, then
install the packages:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

The application checks that the key exists and reports actionable setup
guidance if it is missing or still contains the placeholder value. Keep the
real key private and out of version control; `.gitignore` excludes `.env`.

### Start the chat app

```powershell
python app.py
```

Open the local address reported by Gradio in a browser. The app launches with
sharing disabled.

### Run the command-line smoke test

```powershell
python agent.py
```

This builds the same agent, asks for the current time in London, and prints the
answer in the terminal.

## 7. Configuration

- **Model:** `groq/qwen/qwen3.8-27b` is configured in `build_model()` in
  `agent.py`.
- **Model parameters:** temperature `0.1`; maximum output tokens `2048`.
- **Agent limit:** six steps per run.
- **System prompt:** top-level `system_prompt` in `prompts.yaml`.
- **Credential:** `GROQ_API_KEY` in the process environment or project `.env`.
- **UI sharing:** disabled by `GradioUI(agent).launch(share=False)` in
  `app.py`.

## 8. Implementation approach

The implementation brings the system together in a few focused layers:

1. **Agent framework:** `smolagents` provides the code-oriented agent loop and
   tool interface.
2. **Model connection:** `LiteLLMModel` connects the agent to Groq, keeping the
   model provider configuration separate from the individual tools.
3. **Tool integration:** functions in `tools/custom_tools.py` expose typed,
   documented capabilities to the agent. The `@tool` decorator makes their
   descriptions and input schemas available to the model.
4. **Prompt configuration:** `prompts.yaml` holds the editable system
   instructions separately from Python code.
5. **Application interface:** `app.py` uses the framework's `GradioUI` for a
   local chat experience, while `agent.py` also provides a direct smoke-test
   entry point.
6. **Configuration and dependencies:** `python-dotenv` reads the secret from
   `.env`; `requirements.txt` provides the package manifest; `.gitignore`
   prevents local secrets and generated files from being tracked.

## 9. Operational and security notes

- The API key is required to call Groq. Do not paste it into source files,
  prompts, commits, or public issue reports.
- Open-Meteo lookups require internet access; unavailable services or invalid
  cities may result in an error message returned by the tool.
- The calculator accepts a deliberately limited expression grammar and does
  not execute arbitrary Python expressions.
- `CodeAgent` is designed to execute model-generated code as part of its
  operation. Use this application only with trusted inputs and understand the
  execution configuration of the installed `smolagents` version before
  exposing it to untrusted users.
- Gradio sharing is disabled in the application configuration. This is a
  local-use setting, not authentication or an access-control mechanism.

## 10. Scope and future extensions

The current implementation is intentionally small. Potential future work
could include tests, structured logging, input/output validation, additional
tools, persistent memory, and deployment. Those capabilities should be treated
as future work unless they are added to the codebase; they are not part of the
current system.

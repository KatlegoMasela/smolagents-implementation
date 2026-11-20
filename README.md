# Smolagents Implementation

A Python-based AI agent built using [Hugging Face smolagents](https://github.com/huggingface/smolagents), exploring LLM integration, tool execution, agent reasoning and autonomous task completion.

## Overview

This project focuses on implementing a tool-using AI agent with Python and the Hugging Face smolagents framework.

The agent uses a Large Language Model (LLM) to interpret user instructions, determine which tools are required, execute actions and process the results to generate responses.

The implementation follows the agentic **Think – Act – Observe** cycle, where the agent reasons about a task, executes actions through available tools and observes their outputs before producing a final answer.

The project is based on the [Hugging Face Agents Course – Unit 1](https://huggingface.co/learn/agents-course/unit1/smolagents/first_agent), with additional implementation and experimentation.

## Objectives

- Understand the architecture and execution flow of AI agents.
- Implement a CodeAgent using the smolagents framework.
- Integrate an LLM through Hugging Face Inference Providers.
- Develop and integrate custom Python tools.
- Explore tool calling and code execution.
- Build an interactive interface using Gradio.
- Deploy the application using Hugging Face Spaces.

## Features

The agent is designed to support multiple capabilities through tool integration.

| Capability | Description |
|---|---|
| Web Search | Retrieve information from the web using DuckDuckGo. |
| Time Zone Retrieval | Obtain current local time for specified geographical time zones. |
| Image Generation | Generate images from text prompts using a Hugging Face tool. |
| Tool Execution | Select and execute available tools to complete user instructions. |
| LLM Integration | Use a language model to interpret instructions and coordinate tool usage. |
| Interactive Interface | Interact with the agent through a Gradio-based chat interface. |

*Note: Capabilities depend on which tools have been integrated and configured successfully.*

## Technology Stack

- **Programming Language:** Python
- **Agent Framework:** Hugging Face smolagents
- **LLM Integration:** Hugging Face Inference Providers
- **Language Model:** Qwen2.5-Coder-32B-Instruct (initial model configuration)
- **User Interface:** Gradio
- **Web Search:** DuckDuckGo
- **Time Zone Handling:** pytz
- **Configuration:** YAML
- **Version Control:** Git and GitHub
- **Deployment:** Hugging Face Spaces

## Project Structure

```text
smolagents-implementation/
│
├── tools/
│   ├── __init__.py
│   └── custom_tools.py
│
├── app.py
├── agent.py
├── prompts.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Application entry point and Gradio interface. |
| `agent.py` | Agent configuration, model initialisation and tool registration. |
| `custom_tools.py` | Custom Python tools available to the agent. |
| `prompts.yaml` | System prompts and instructions governing agent behaviour. |
| `requirements.txt` | Project dependencies. |
| `.env.example` | Example environment variable configuration. |
| `.gitignore` | Excludes sensitive and unnecessary files. |

## Installation and Setup

### Prerequisites

Ensure the following are installed:

- Python 3.11 or later.
- Git.
- Visual Studio Code or another Python-compatible IDE.
- A GitHub account.
- A Hugging Face account with access to Inference Providers.

### 1. Clone the repository

```bash
git clone https://github.com/KatlegoMasela/smolagents-implementation.git

cd smolagents-implementation
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory.

Add your Hugging Face access token:

```env
HF_TOKEN=your_hugging_face_token
```

Generate a token from:

https://huggingface.co/settings/tokens

Never commit your actual API token or `.env` file to GitHub.

### 5. Run the application

```bash
python app.py
```

Open the local application in your browser:

http://127.0.0.1:7860

## Agent Architecture

The application uses the smolagents CodeAgent architecture.

The execution process follows these stages:

1. **User Input:** The user submits an instruction through the Gradio interface.
2. **Reasoning:** The LLM interprets the instruction and determines the appropriate actions.
3. **Tool Selection:** The agent selects an available tool based on the task.
4. **Action Execution:** The agent executes the required tool or code.
5. **Observation:** The agent evaluates the output returned by the tool.
6. **Final Response:** The agent processes the results and generates a response.

## Example Use Cases

The agent can be tested with instructions such as:

**Web Search**

> Search for recent developments in artificial intelligence and summarise the key findings.

**Time Zone Retrieval**

> What is the current time in London?

**Image Generation**

> Generate an image of a futuristic artificial intelligence research laboratory.

These examples demonstrate how an agent can use external tools to perform tasks beyond ordinary text generation.

## Development and Future Improvements

Planned areas of exploration include:

- Developing additional custom Python tools.
- Integrating external REST APIs.
- Experimenting with different LLMs.
- Improving system prompts and agent instructions.
- Implementing more robust error handling and logging.
- Adding input validation and output verification.
- Exploring agent memory and multi-agent architectures.
- Evaluating agent performance and tool execution reliability.
- Improving security through sandboxed code execution.

## Deployment

The application is intended for deployment through [Hugging Face Spaces](https://huggingface.co/spaces).

Deployment requires:

1. Creating a Gradio-based Hugging Face Space.
2. Configuring the required Python dependencies.
3. Adding `HF_TOKEN` under the Space's Secrets settings.
4. Deploying the application files.
5. Verifying the application through the hosted interface.

## Learning Reference

This implementation is part of the [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit1/smolagents/first_agent).

Additional documentation:

- [smolagents Documentation](https://huggingface.co/docs/smolagents/index)
- [smolagents GitHub Repository](https://github.com/huggingface/smolagents)
- [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/index)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/en/spaces)

## Author

**Katlego Masela**

BSc Information Technology Graduate

- [GitHub](https://github.com/KatlegoMasela)
- [LinkedIn](https://www.linkedin.com/in/katlego-masela-910613273/)

---

*This repository serves as a practical exploration of Python-based AI agent development, LLM integration and tool-using autonomous systems.*
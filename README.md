# AI Agent Project

A simple AI agent implementation using OpenAI's GPT-3.5-turbo model. The agent can perform basic tasks using tools like search and calculator functions.

## Features

- Search tool: Currently provides information about France's capital
- Calculator tool: Performs basic mathematical calculations
- OpenAI GPT-3.5-turbo integration
- Simple tool response handling

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/ai_agent_project.git
cd ai_agent_project
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

5. Run the agent:
```bash
python agent.py
```

## Example Usage

The agent can handle queries like:
- "What is the capital of France?"
- "What is 2 + 2?"

## Project Structure

- `agent.py`: Main agent implementation with tool definitions
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (not tracked in git)

## License

MIT License 
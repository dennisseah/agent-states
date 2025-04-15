# agent-states
managing agent states in a agentic AI system

## Setup

1. Clone the repository
2. `cd agent-states` (root directory of this git repository)
3. `uv sync`
6. `pre-commit install` (install the pre-commit hooks)
4. code . (open the project in vscode)
5. install the recommended extensions (cmd + shift + p -> `Extensions: Show Recommended Extensions`)
7. copy the `.env.sample` file to `.env` and fill in the values

## Samples
```sh
python -m agent_states.graph
```

## Unit Test Coverage

```sh
python -m pytest -p no:warnings --cov-report term-missing --cov=agent_states tests
```


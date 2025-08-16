# Agentic PR Descriptions

## Overview

Agentic PR Descriptions is a command-line tool that automatically generates a pull request (PR) description based on the diff between two Git branches. It uses the `crewai` framework to leverage AI agents for generating a comprehensive and informative summary of the changes.

This tool is designed to be run in a local Git repository. It computes the diff (patch) between a feature branch and a base branch, and then uses that diff as context for an AI agent to write a descriptive PR summary.

## Features

*   **Automatic Diff Generation:** Automatically computes the diff between your feature branch and a base branch (e.g., `main` or `master`).
*   **AI-Powered Descriptions:** Uses AI agents to generate a clear and concise PR description from the code changes.
*   **Local Repository Support:** Runs directly on your local Git repository.
*   **Customizable Branch Comparison:** Allows you to specify both the feature and base branches for comparison.

## Installation & Setup

This project is developed using Python 3.13 and `uv`.

1.  **Install `uv`**: If you don't already have it, install `uv` by following the official instructions: https://docs.astral.sh/uv/

2.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

3.  **Create Environment and Install Dependencies**:
    The `uv sync` command is the most efficient way to set up your project. It automatically creates a virtual environment in the current directory (in a `.venv` folder) if one doesn't exist, and installs all dependencies from your `pyproject.toml` file.
    Once you have `uv` installed, simply run:
    ```bash
    uv sync
    ```

4.  **Activate the Virtual Environment**:
    Once the sync is complete, activate the new environment to use the installed packages:
    ```bash
    source .venv/bin/activate
    ```

## Usage

The script is run from the command line and accepts arguments to specify the repository path and branches to compare.

### Command-Line Interface

The main script `main.py` provides the following command-line arguments:

| Argument | Description | Required | Default |
| :--- | :--- | :---: | :---: |
| `--repo_path` | The file system path to the local Git repository. | Yes | |
| `--feature_branch` | The name of the feature branch (the 'new' code). | Yes | |
| `--base_branch` | The name of the base branch to compare against. | No | `main` |

### Example

To generate a PR description for a feature branch named `feat/new-login-flow` in a repository located at `~/projects/my-app`, run the following command:

```bash
python main.py \
  --repo_path ~/projects/my-app \
  --feature_branch feat/new-login-flow \
  --base_branch main
```

The generated PR description will be printed to the console and saved to `pr_description.md`.

## CrewAI Configuration

The behavior of the AI is defined in external configuration files (e.g., `config/agents.yaml` and `config/tasks.yaml`), making it easy to customize without changing the Python code.

*   **Agent Configuration (`pr_description_agent`)**: The agent is configured with the persona of a "Senior Software Developer AI Assistant." Its goal is to meticulously analyze code changes from a git diff and write a professional PR description. Its backstory emphasizes relying solely on the provided diff content, without access to external tools.

*   **Task Configuration (`generate_pr_description_task`)**: The task provides the agent with the git diff and instructs it to generate a markdown description. It enforces a strict template that includes sections for `Context`, `Description`, `Technical notes`, `User-facing changes`, and `Tests`. This ensures that all generated descriptions are consistent and comprehensive.

You can modify these configuration files to change the agent's persona, adjust the instructions, or alter the final markdown template to fit your team's specific needs.

## Key Libraries and References

This project relies on several key libraries to function. Below are links to their official documentation:

*   **CrewAI**: A framework for orchestrating role-playing, autonomous AI agents.
    *   [Documentation](https://docs.crewai.com/)
*   **uv**: An extremely fast Python package installer and resolver, written in Rust.
    *   [Documentation](https://docs.astral.sh/uv/)
*   **GitPython**: A Python library used to interact with Git repositories.
    *   [Documentation](https://gitpython.readthedocs.io/en/stable/)

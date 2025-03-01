# Installation Guide

This guide will help you set up the Conway Bio project, which integrates the `lifegame` package with a GitHub bio updater.

## Prerequisites

- [mise](https://mise.jdx.dev/) - A dev tool manager that handles Python versions and virtual environments
- [uv](https://github.com/astral-sh/uv) - A fast Python package installer and resolver (installed automatically by mise)

## Installation Steps

### 1. Install mise

If you don't have mise installed, you can install it using:

```bash
# macOS with Homebrew
brew install mise

# Or using the installer script
curl https://mise.run | sh
```

For other installation methods, see the [mise documentation](https://mise.jdx.dev/getting-started.html).

### 2. Clone the Repository

```bash
git clone https://github.com/codekiln/codekiln.git
cd codekiln
```

### 3. Install Dependencies

The project uses mise to manage Python versions and dependencies. Simply run:

```bash
mise run install
```

This command will:
1. Create a Python virtual environment
2. Install the lifegame package in development mode
3. Install the root package and its dependencies

### 4. Configure GitHub Token

To run the Conway Bio updater, you need a GitHub Personal Access Token with the `user` scope:

1. Create a token at [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Create a `.env` file in the project root with the following content:
   ```
   PAT_GITHUB=your_github_token_here
   ```

## Running the Project

### Run the Conway Bio Updater

```bash
mise run run
```

This will fetch your current GitHub bio, evolve it according to Conway's Game of Life rules, and update it.

### Run Tests

```bash
mise run test
```

## Development

### Project Structure

- `conway-bio.py` - The main script that updates GitHub bios
- `lifegame/` - The package implementing Conway's Game of Life
- `.mise.toml` - Configuration for mise, including tasks and environment variables

### Adding Dependencies

To add new dependencies:

1. Add them to the appropriate section in `pyproject.toml`
2. Run `mise run install` to install them

### Virtual Environment

The project uses mise's built-in virtual environment support. The virtual environment is automatically activated when you run any mise command in the project directory.

### IDE Setup

#### VSCode / Cursor

The repository includes VSCode/Cursor settings to use the mise-managed virtual environment:

1. Open the project in VSCode or Cursor
2. The editor should automatically detect the Python interpreter in `.venv/bin/python`
3. If not, you can manually select it:
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Python: Select Interpreter"
   - Choose the interpreter at `.venv/bin/python`

For manual configuration, you can add these settings to your `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.extraPaths": [
        "${workspaceFolder}",
        "${workspaceFolder}/lifegame"
    ],
    "python.terminal.activateEnvironment": true
}
```

## Troubleshooting

### Missing Dependencies

If you encounter "ModuleNotFoundError", try reinstalling dependencies:

```bash
mise run install
```

### GitHub API Issues

If you encounter issues with the GitHub API:
1. Check that your PAT_GITHUB token is valid and has the correct permissions
2. Ensure you haven't exceeded GitHub API rate limits

### Python Version Issues

If you encounter Python version compatibility issues:
1. Check that you have Python 3.12 installed (mise should handle this automatically)
2. Try running `mise use python@3.12` to explicitly set the Python version 
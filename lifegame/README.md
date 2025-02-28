# lifegame

A Python package implementing Conway's Game of Life with multiple rule variations and rendering modes.

## Features

- Multiple rule variations (Standard Conway, Day & Night, HighLife)
- Advanced rendering modes (full block and half block characters)
- Flexible command-line interface
- Toroidal (wraparound) grid behavior

## Installation

```bash
pip install lifegame
```

## Usage

### Command Line Interface

The package provides a command-line interface for running Conway's Game of Life simulations with various configurations.

Basic usage:

```bash
lifegame-run --width 20 --height 10 --iterations 50 --delay 0.2 --rules standard --display full
```

#### Available Options

- `--width`: Width of the grid (default: 20)
- `--height`: Height of the grid (default: 10)
- `--iterations`: Number of iterations to run (default: 50)
- `--delay`: Delay between iterations in seconds (default: 0.2)
- `--rules`: Rule set to use (choices: standard, daynight, highlife; default: standard)
- `--display`: Display mode to use (choices: full, half; default: full)
- `--input`: Path to a file containing the initial grid
- `--random`: Generate a random initial grid

For help and all available options:

```bash
lifegame-run --help
```

### Examples

#### Running with Different Rule Sets

Standard Conway rules:
```bash
lifegame-run --rules standard
```

Day & Night rules:
```bash
lifegame-run --rules daynight
```

HighLife rules:
```bash
lifegame-run --rules highlife
```

#### Using Different Display Modes

Full block rendering (standard resolution):
```bash
lifegame-run --display full
```

Half block rendering (doubled vertical resolution):
```bash
lifegame-run --display half
```

#### Loading Custom Patterns

From a file:
```bash
lifegame-run --input patterns/glider.txt
```

Generate a random grid:
```bash
lifegame-run --random --width 30 --height 15
```

### Grid File Format

When creating custom grid files, use the following format:
- Use `1` or `█` for alive cells
- Use `0` or space for dead cells
- Ensure all rows have the same width

Example (glider pattern):
```
 █ 
  █
███
```

## Development

To set up the development environment:

1. Clone the repository
2. Install poetry if not already installed: `pip install poetry`
3. Install dependencies: `poetry install`
4. Run tests: `poetry run pytest`

### Running Tests

To run all tests:
```bash
poetry run pytest
```

To run tests with verbose output:
```bash
poetry run pytest -v
```

To run specific test files:
```bash
poetry run pytest tests/test_game.py
```

## License

See the LICENSE file in the root directory for license information. 
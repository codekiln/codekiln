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

Basic usage from the command line:

```bash
lifegame-run --width 18 --height 8 --iterations 1 --rules standard --display full
```

For more options, use:

```bash
lifegame-run --help
```

## Development

To set up the development environment:

1. Clone the repository
2. Install poetry if not already installed: `pip install poetry`
3. Install dependencies: `poetry install`
4. Run tests: `poetry run pytest`

## License

See the LICENSE file in the root directory for license information. 
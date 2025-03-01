# Conway Bio Usage Guide

This guide explains how to use the `conway-bio.py` script to update your GitHub bio with Conway's Game of Life patterns.

## Basic Usage

```bash
python conway-bio.py
```

This will:
1. Fetch your current GitHub bio
2. Evolve it according to Conway's Game of Life rules
3. Update your GitHub bio with the new pattern

## Command-Line Options

### Grid Dimensions

The script uses a default grid size of 5 rows × 33 columns, but you can customize this:

```bash
# Set custom number of rows
python conway-bio.py --rows 4

# Set custom number of columns
python conway-bio.py --columns 30

# Set maximum character length (default is 160)
python conway-bio.py --max-length 100
```

**Note:** GitHub bio has a maximum character limit of 160. If your grid exceeds this limit, the script will truncate it and display a warning.

### Game Rules

```bash
# Use standard Conway's Game of Life rules (default)
python conway-bio.py --rules standard

# Use HighLife rules (similar to standard but with an additional birth rule)
python conway-bio.py --rules highlife

# Use Day & Night rules (a more complex ruleset)
python conway-bio.py --rules daynight
```

### Display Modes

```bash
# Use full display mode with block characters (default)
python conway-bio.py --display full

# Use half display mode with white/black circle characters
python conway-bio.py --display half
```

### Randomization

```bash
# Randomize the board based on the current day (creates a consistent pattern for each day)
python conway-bio.py --random-by-day

# Randomize the board with a specific density (0.0 to 1.0, where higher values create more live cells)
python conway-bio.py --randomize-board 0.3
```

### Preview Mode

```bash
# Preview the evolution for a specific number of iterations without updating GitHub
python conway-bio.py --preview 5
```

### Input File

```bash
# Use a specific file as input instead of fetching from GitHub
python conway-bio.py --input my_pattern.txt
```

## Examples

```bash
# Preview 3 iterations of a random board with 30% live cells
python conway-bio.py --preview 3 --randomize-board 0.3

# Use a 4×30 grid with HighLife rules
python conway-bio.py --rows 4 --columns 30 --rules highlife

# Create a pattern that changes daily and preview it
python conway-bio.py --random-by-day --preview 2

# Use minimal display mode with a maximum length of 100 characters
python conway-bio.py --display half --max-length 100
```

## GitHub Bio Integration

For the script to update your GitHub bio, you need to:

1. Create a GitHub Personal Access Token with the `user` scope
2. Set it in a `.env` file as `PAT_GITHUB=your_token_here`

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions. 
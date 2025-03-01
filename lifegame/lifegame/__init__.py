"""lifegame package."""

__version__ = "0.1.0"

# Import main CLI entry point
# Import key functions from bio module
from lifegame.bio import (
    calculate_safe_dimensions,
    format_grid_for_bio,
    get_random_options_by_day,
    parse_bio_to_grid,
)
from lifegame.cli import main

# Import key functions from game module
from lifegame.game import (
    get_neighbors,
    load_grid_from_string,
    next_cell_state,
    render_full,
    render_half,
    step,
)

# Define what's available when using "from lifegame import *"
__all__ = [
    # CLI
    "main",
    # Game logic
    "load_grid_from_string",
    "get_neighbors",
    "next_cell_state",
    "step",
    "render_full",
    "render_half",
    # Bio integration
    "calculate_safe_dimensions",
    "format_grid_for_bio",
    "get_random_options_by_day",
    "parse_bio_to_grid",
]

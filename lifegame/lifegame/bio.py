"""
GitHub Bio integration for Conway's Game of Life.

This module provides functions for integrating Conway's Game of Life with GitHub bios.
It handles parsing GitHub bios as game grids, formatting grids for display in GitHub bios,
and other bio-specific functionality.

The module addresses specific challenges with GitHub bio rendering, such as:
- Character width consistency in non-monospaced fonts
- Maximum bio length limitations (160 characters)
- Proper formatting for visual appeal
"""

__all__ = [
    "parse_bio_to_grid",
    "format_grid_for_bio",
    "calculate_safe_dimensions",
    "get_random_options_by_day",
]

import datetime
from typing import Dict, List, Tuple

from lifegame.constants import (
    ALIVE_CHARS,
    EMPTY_CHAR,
    FULL_CHAR,
    NEWLINE_CHAR,
    TALL_BLOCK_CHAR,
)
from lifegame.game import render_full, render_half


def parse_bio_to_grid(
    current_bio: str, rows: int, cols: int
) -> Tuple[List[List[int]], bool]:
    """
    Parse a GitHub bio string into a Conway's Game of Life grid.

    Args:
        current_bio (str): The GitHub bio string
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid

    Returns:
        tuple: (grid, is_valid) where grid is a 2D list and is_valid indicates if the grid was valid
    """
    # Check if the bio is a flat string (no newlines) that needs to be inflated
    if NEWLINE_CHAR not in current_bio and len(current_bio) > 0:
        # Calculate how many complete rows we can fill
        complete_rows = len(current_bio) // cols
        remainder = len(current_bio) % cols

        # Reconstruct the bio with newlines
        board_lines = []
        for i in range(complete_rows):
            board_lines.append(current_bio[i * cols : (i + 1) * cols])

        # Add the remainder as a partial row if any
        if remainder > 0:
            partial_row = current_bio[complete_rows * cols :] + EMPTY_CHAR * (
                cols - remainder
            )
            board_lines.append(partial_row)

        # Fill in any remaining rows with dead cells
        while len(board_lines) < rows:
            board_lines.append(EMPTY_CHAR * cols)

        # Join with newlines to create a properly formatted bio
        current_bio = NEWLINE_CHAR.join(board_lines)

    # Now parse the bio as before
    lines = current_bio.split(NEWLINE_CHAR)
    board_lines = lines[:rows]  # Use the first 'rows' lines

    # Validate that we have the expected number of lines with correct width
    valid = True
    if len(board_lines) < rows:
        valid = False
        # Pad with empty rows if we have fewer than expected
        board_lines.extend([EMPTY_CHAR * cols] * (rows - len(board_lines)))
    else:
        for i, line in enumerate(board_lines):
            # Ensure each line has exactly 'cols' characters
            if len(line) != cols:
                valid = False
                # Pad or truncate the line to match cols
                if len(line) < cols:
                    board_lines[i] = line + EMPTY_CHAR * (cols - len(line))
                else:
                    board_lines[i] = line[:cols]

    # If completely invalid (e.g., empty bio), seed a default glider board
    if not valid and len("".join(board_lines).strip()) == 0:
        # Create a default glider in the top-left corner
        board_lines = [EMPTY_CHAR * cols for _ in range(rows)]
        if cols >= 3 and rows >= 3:
            board_lines[0] = (
                EMPTY_CHAR + FULL_CHAR + EMPTY_CHAR + EMPTY_CHAR * (cols - 3)
            )
            board_lines[1] = (
                EMPTY_CHAR + EMPTY_CHAR + FULL_CHAR + EMPTY_CHAR * (cols - 3)
            )
            board_lines[2] = FULL_CHAR + FULL_CHAR + FULL_CHAR + EMPTY_CHAR * (cols - 3)

    # Create a 2D grid directly for the lifegame package
    # Convert "■" to 1 (alive), "▀" and "▄" to 1 (alive), and "□" to 0 (dead)
    grid = []
    for line in board_lines:
        row = []
        for i, cell in enumerate(line):
            if i < rows:
                row.append(1 if cell in ALIVE_CHARS else 0)

        grid.append(row)

    return grid, valid


def format_grid_for_bio(
    grid: List[List[int]], display_mode: str = "full", max_length: int = 160
) -> Tuple[str, str]:
    """
    Format a grid for display in a GitHub bio.

    Args:
        grid (list): 2D list representing the grid
        display_mode (str): Display mode to use (full or half)
        max_length (int): Maximum length of the bio

    Returns:
        tuple: (github_bio, display_bio) where github_bio is a flat string for GitHub
               and display_bio is a formatted string with newlines for display
    """
    # Select the appropriate rendering function
    render_func = render_full if display_mode == "full" else render_half

    # Convert the grid to a string
    rendered_grid = render_func(grid)

    # Convert the rendered output to the format used in the bio
    if display_mode == "full":
        # For full mode, replace "█" with "■" and spaces with "□"
        # Note: We're using "■" instead of "█" for better width consistency in GitHub bios
        formatted_grid = rendered_grid.replace(TALL_BLOCK_CHAR, FULL_CHAR).replace(
            " ", EMPTY_CHAR
        )
    else:
        # For half mode, keep the half blocks and replace spaces with "□"
        formatted_grid = rendered_grid.replace(" ", EMPTY_CHAR)

    # Create a display version with newlines for preview purposes
    display_version = formatted_grid

    # Ensure the bio doesn't exceed the maximum length
    # total_chars = len(formatted_grid.replace(NEWLINE_CHAR, ""))
    # if total_chars > max_length:
    #     # Truncate the bio if necessary, but preserve the original format
    #     # Just take the first max_length characters (flattened)
    #     # flat_bio = formatted_grid.replace(NEWLINE_CHAR, "")
    #     flat_bio = formatted_grid
    #     truncated_bio = flat_bio[:max_length]

    #     # For GitHub, we'll send the truncated flat string
    #     formatted_grid = truncated_bio
    # else:
    #     # For GitHub, we'll send the flat string without newlines
    #     # formatted_grid = formatted_grid.replace(NEWLINE_CHAR, "")
    #     pass

    # Return both the GitHub version (flat string) and the display version (with newlines)
    return formatted_grid, display_version


def calculate_safe_dimensions(
    rows: int, columns: int, max_length: int, display_mode: str = "full"
) -> Tuple[int, int]:
    """
    Calculate safe dimensions that will fit within the maximum length.

    Args:
        rows (int): Requested number of rows
        columns (int): Requested number of columns
        max_length (int): Maximum length of the bio
        display_mode (str): Display mode to use (full or half)

    Returns:
        tuple: (safe_rows, safe_columns) that will fit within max_length
    """
    total_chars = rows * columns

    # If the dimensions already fit, return them unchanged
    if total_chars <= max_length:
        return rows, columns

    # Calculate maximum dimensions that would fit
    if display_mode == "half":
        # In half mode, we can fit approximately twice as many cells
        # since each row is half the height
        effective_max = max_length * 2

        # Try to maintain the requested number of columns
        if columns <= effective_max:
            safe_rows = min(rows, effective_max // columns)
            safe_columns = columns
        else:
            # If columns alone exceed the limit, reduce them
            safe_rows = 1
            safe_columns = effective_max
    else:
        # In full mode, calculate dimensions that would fit
        if rows <= 1:
            # Single row case
            safe_rows = 1
            safe_columns = min(columns, max_length)
        else:
            # Try to maintain aspect ratio
            safe_rows = min(rows, max(1, int(max_length / columns)))
            safe_columns = min(columns, max_length // safe_rows)

    return safe_rows, safe_columns


def get_random_options_by_day() -> Dict[str, str]:
    """
    Select random options based on the day of the year.

    Returns:
        dict: Dictionary with randomly selected options
    """
    # Get the day of the year (1-366)
    day_of_year = datetime.datetime.now().timetuple().tm_yday

    # Available rule sets and display modes
    rule_sets = ["standard", "daynight", "highlife"]
    display_modes = ["full", "half"]

    # Use the day of year to select options
    selected_rule = rule_sets[day_of_year % len(rule_sets)]
    selected_display = display_modes[
        (day_of_year // len(rule_sets)) % len(display_modes)
    ]

    return {
        "rules": selected_rule,
        "display": selected_display,
    }

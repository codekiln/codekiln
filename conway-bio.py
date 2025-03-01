#!/usr/bin/env python3
"""
Conway Bio Updater

This script updates a GitHub user's bio with a Conway's Game of Life grid that evolves
with each run. It uses the lifegame package to handle the grid evolution logic.

The script:
1. Fetches the current GitHub bio
2. Parses it as a Conway's Game of Life grid (default: 33x5)
3. Evolves the grid one step using the lifegame package
4. Updates the bio with the new grid

Command-line options:
  --rules {standard,daynight,highlife}  Rule set to use (default: standard)
  --display {full,half}                 Display mode to use (default: half)
  --random-by-day                       Select options based on day of year
  --randomize-board [DENSITY]           Generate a random initial board
  --preview [ITERATIONS]                Preview evolution without updating bio
  --input FILE                          Load initial grid from file
  --rows ROWS                           Number of rows in the grid (default: 5)
  --columns COLUMNS                     Number of columns in the grid (default: 33)
  --max-length LENGTH                   Maximum bio length (default: 160)

The script requires a GitHub Personal Access Token (PAT) with the 'user' scope,
which can be provided via the PAT_GITHUB environment variable.

Note: GitHub bio has a maximum of 160 characters. The default grid (33x5=165)
slightly exceeds this, but the script handles this by treating the last few cells
as permanently dead.
"""

import argparse
import datetime
import getpass
import os
import sys
import time

import requests

# Import the necessary functions from the lifegame package
from lifegame import load_grid_from_string, render_full, render_half, step
from lifegame.cli import generate_random_grid

# Only try to load dotenv if not running in GitHub Actions
if "GITHUB_ACTIONS" not in os.environ:
    from dotenv import load_dotenv

    load_dotenv()

# Default constants for grid dimensions
DEFAULT_ROWS = 5
DEFAULT_COLS = 33
DEFAULT_MAX_LENGTH = 160


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Update GitHub bio with Conway's Game of Life grid."
    )

    # Rule set options
    parser.add_argument(
        "--rules",
        type=str,
        default="standard",
        choices=["standard", "daynight", "highlife"],
        help="Rule set to use (default: standard)",
    )

    # Display mode options
    parser.add_argument(
        "--display",
        type=str,
        default="half",
        choices=["full", "half"],
        help="Display mode to use (default: half)",
    )

    # Random options
    parser.add_argument(
        "--random-by-day",
        action="store_true",
        help="Select options based on day of year",
    )

    parser.add_argument(
        "--randomize-board",
        nargs="?",
        const=0.3,
        type=float,
        metavar="DENSITY",
        help="Generate a random initial board with specified density (0.0-1.0, default: 0.3)",
    )

    # Preview mode
    parser.add_argument(
        "--preview",
        nargs="?",
        const=5,
        type=int,
        metavar="ITERATIONS",
        help="Preview evolution without updating bio (default: 5 iterations)",
    )

    # Input file
    parser.add_argument(
        "--input",
        type=str,
        help="Path to a file containing the initial grid",
    )

    # Grid dimensions
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROWS,
        help=f"Number of rows in the grid (default: {DEFAULT_ROWS})",
    )

    parser.add_argument(
        "--columns",
        type=int,
        default=DEFAULT_COLS,
        help=f"Number of columns in the grid (default: {DEFAULT_COLS})",
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=DEFAULT_MAX_LENGTH,
        help=f"Maximum bio length (default: {DEFAULT_MAX_LENGTH})",
    )

    return parser.parse_args()


def get_random_options_by_day():
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


def calculate_safe_dimensions(rows, columns, max_length, display_mode="full"):
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


def load_grid_from_file(file_path):
    """
    Load a grid from a file.

    Args:
        file_path (str): Path to the file containing the grid

    Returns:
        list: The loaded grid
    """
    try:
        with open(file_path, "r") as f:
            grid_str = f.read()
        return load_grid_from_string(grid_str)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing grid from file: {e}")
        sys.exit(1)


def parse_bio_to_grid(current_bio, rows, cols):
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
    if "\n" not in current_bio and len(current_bio) > 0:
        # Calculate how many complete rows we can fill
        complete_rows = len(current_bio) // cols
        remainder = len(current_bio) % cols

        # Reconstruct the bio with newlines
        board_lines = []
        for i in range(complete_rows):
            board_lines.append(current_bio[i * cols : (i + 1) * cols])

        # Add the remainder as a partial row if any
        if remainder > 0:
            partial_row = current_bio[complete_rows * cols :] + "□" * (cols - remainder)
            board_lines.append(partial_row)

        # Fill in any remaining rows with dead cells
        while len(board_lines) < rows:
            board_lines.append("□" * cols)

        # Join with newlines to create a properly formatted bio
        current_bio = "\n".join(board_lines)

    # Now parse the bio as before
    lines = current_bio.split("\n")
    board_lines = lines[:rows]  # Use the first 'rows' lines

    # Validate that we have the expected number of lines with correct width
    valid = True
    if len(board_lines) < rows:
        valid = False
        # Pad with empty rows if we have fewer than expected
        board_lines.extend(["□" * cols] * (rows - len(board_lines)))
    else:
        for i, line in enumerate(board_lines):
            # Ensure each line has exactly 'cols' characters
            if len(line) != cols:
                valid = False
                # Pad or truncate the line to match cols
                if len(line) < cols:
                    board_lines[i] = line + "□" * (cols - len(line))
                else:
                    board_lines[i] = line[:cols]

    # If completely invalid (e.g., empty bio), seed a default glider board
    if not valid and len("".join(board_lines).strip()) == 0:
        # Create a default glider in the top-left corner
        board_lines = ["□" * cols for _ in range(rows)]
        if cols >= 3 and rows >= 3:
            board_lines[0] = "□▀□" + "□" * (cols - 3)
            board_lines[1] = "□□▀" + "□" * (cols - 3)
            board_lines[2] = "▀▀▀" + "□" * (cols - 3)

    # Create a 2D grid directly for the lifegame package
    # Convert "■" to 1 (alive), "▀" and "▄" to 1 (alive), and "□" to 0 (dead)
    grid = []
    for line in board_lines:
        row = [1 if cell in "■▀▄" else 0 for cell in line]
        grid.append(row)

    return grid, valid


def format_grid_for_bio(grid, display_mode="half", max_length=DEFAULT_MAX_LENGTH):
    """
    Format a grid for display in a GitHub bio.

    Args:
        grid (list): 2D list representing the grid
        display_mode (str): Display mode to use (full or half)
        max_length (int): Maximum length of the bio

    Returns:
        str: Formatted grid string for GitHub bio
    """
    # Select the appropriate rendering function
    render_func = render_full if display_mode == "full" else render_half

    # Convert the grid to a string
    rendered_grid = render_func(grid)

    # Convert the rendered output to the format used in the bio
    if display_mode == "full":
        # For full mode, replace "█" with "■" and spaces with "□"
        formatted_grid = rendered_grid.replace("█", "■").replace(" ", "□")
    else:
        # For half mode, keep the half blocks and replace spaces with "□"
        formatted_grid = rendered_grid.replace(" ", "□")

    # Create a display version with newlines for preview purposes
    display_version = formatted_grid

    # Ensure the bio doesn't exceed the maximum length
    total_chars = len(formatted_grid.replace("\n", ""))
    if total_chars > max_length:
        print(f"Warning: Bio exceeds maximum length of {max_length} characters.")
        print(f"Current length: {total_chars} characters.")
        print(
            f"The bio will be truncated to {max_length} characters when sent to GitHub."
        )
        print(
            "When retrieved, it will be inflated back to the original dimensions with dead cells."
        )

        # Truncate the bio if necessary, but preserve the original format
        # Just take the first max_length characters (flattened)
        flat_bio = formatted_grid.replace("\n", "")
        truncated_bio = flat_bio[:max_length]

        # For GitHub, we'll send the truncated flat string
        formatted_grid = truncated_bio
    else:
        # For GitHub, we'll send the flat string without newlines
        formatted_grid = formatted_grid.replace("\n", "")

    # Return both the GitHub version (flat string) and the display version (with newlines)
    return formatted_grid, display_version


def preview_evolution(
    grid, iterations=5, rule_set="standard", display_mode="full", delay=0.5
):
    """
    Preview the evolution of a grid without updating the GitHub bio.

    Args:
        grid (list): Initial grid state
        iterations (int): Number of iterations to run
        rule_set (str): Rule set to use
        display_mode (str): Display mode to use
        delay (float): Delay between iterations in seconds
    """
    # Select the appropriate rendering function
    render_func = render_full if display_mode == "full" else render_half

    # Display the initial grid
    print(f"\nInitial grid (Rule set: {rule_set}, Display mode: {display_mode}):")
    print(render_func(grid))

    # Run the simulation for the specified number of iterations
    for i in range(iterations):
        # Wait for the specified delay
        time.sleep(delay)

        # Evolve the grid one step
        grid = step(grid, rule_set=rule_set)

        # Display the updated grid
        print(f"\nIteration {i + 1}/{iterations}:")
        print(render_func(grid))

    return grid


def update_github_bio(pat, bio_content):
    """
    Update the GitHub bio with the provided content.

    Args:
        pat (str): GitHub Personal Access Token
        bio_content (str): New bio content

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {pat}",
        }

        payload = {"bio": bio_content}
        response = requests.patch(
            "https://api.github.com/user", headers=headers, json=payload
        )
        response.raise_for_status()

        print("\nBio updated successfully!")
        return True

    except requests.exceptions.RequestException as e:
        print(f"GitHub API error: {e}")
        return False


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Apply random-by-day option if specified
    if args.random_by_day:
        random_options = get_random_options_by_day()
        print("Random options selected based on day of year:")
        print(f"  - Rule set: {random_options['rules']}")
        print(f"  - Display mode: {random_options['display']}")

        # Override the command-line arguments
        args.rules = random_options["rules"]
        args.display = random_options["display"]

    # Check if grid dimensions exceed max length
    total_chars = args.rows * args.columns
    if total_chars > args.max_length:
        print(
            f"Warning: Grid dimensions ({args.rows}x{args.columns}={total_chars}) exceed max length ({args.max_length})."
        )
        print(
            f"The bio will be truncated to {args.max_length} characters when sent to GitHub."
        )
        print(
            "When retrieved, it will be inflated back to the original dimensions with dead cells."
        )

        # We no longer adjust dimensions - we'll keep the original dimensions
        # and just truncate when sending to GitHub

    # Read PAT from environment variable "PAT_GITHUB"
    pat = os.getenv("PAT_GITHUB")
    if not pat and not args.preview:
        # Fall back to prompt if not set, without echoing the input.
        pat = getpass.getpass("Enter your GitHub PAT (it will not be echoed): ")

    try:
        # Initialize the grid
        grid = None

        # Option 1: Load from file
        if args.input:
            print(f"Loading grid from file: {args.input}")
            grid = load_grid_from_file(args.input)

            # Resize the grid if necessary
            if len(grid) != args.rows or len(grid[0]) != args.columns:
                print(
                    f"Resizing grid from {len(grid)}x{len(grid[0])} to {args.rows}x{args.columns}"
                )

                # Create a new grid with the specified dimensions
                new_grid = [[0 for _ in range(args.columns)] for _ in range(args.rows)]

                # Copy as much of the original grid as possible
                for y in range(min(len(grid), args.rows)):
                    for x in range(min(len(grid[0]), args.columns)):
                        new_grid[y][x] = grid[y][x]

                grid = new_grid

        # Option 2: Generate random board
        elif args.randomize_board is not None:
            density = args.randomize_board
            print(f"Generating random board with density: {density}")
            grid = generate_random_grid(args.columns, args.rows, density)

        # Option 3: Fetch from GitHub bio (default)
        elif not args.preview:
            # GET /user to read current bio
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {pat}",
            }
            response = requests.get("https://api.github.com/user", headers=headers)
            response.raise_for_status()

            user_data = response.json()
            current_bio = user_data.get("bio") or ""

            # Parse the bio into a grid
            grid, is_valid = parse_bio_to_grid(current_bio, args.rows, args.columns)

            if not is_valid:
                print("Warning: Bio format was invalid or empty. Using default grid.")

        # If we still don't have a grid (e.g., preview mode without other options),
        # create a default glider
        if grid is None:
            print("Using default glider grid")
            grid = [[0 for _ in range(args.columns)] for _ in range(args.rows)]

            # Add a glider in the top-left corner if there's enough space
            if args.columns >= 3 and args.rows >= 3:
                grid[0][1] = 1
                grid[1][2] = 1
                grid[2][0] = grid[2][1] = grid[2][2] = 1

        # Debug output to show grid dimensions
        print(f"Input grid dimensions: {len(grid)} rows x {len(grid[0])} columns")

        # Preview mode: show multiple iterations without updating bio
        if args.preview:
            iterations = args.preview
            final_grid = preview_evolution(
                grid,
                iterations=iterations,
                rule_set=args.rules,
                display_mode=args.display,
            )

            # Format the final grid for display
            github_bio, display_bio = format_grid_for_bio(
                final_grid, args.display, args.max_length
            )
            print("\nFinal grid (formatted for bio):")
            print(display_bio)

            print("\nActual content sent to GitHub (without newlines):")
            print(github_bio)

            # Exit without updating bio
            return

        # Normal mode: evolve the grid one step and update bio
        new_grid = step(grid, rule_set=args.rules)

        # Format the grid for the bio
        github_bio, display_bio = format_grid_for_bio(
            new_grid, args.display, args.max_length
        )

        # Debug output to show the result
        print("\nOutput grid (as displayed on GitHub):")
        print(display_bio)

        print("\nActual content sent to GitHub (without newlines):")
        print(github_bio)

        # Update the GitHub bio
        update_github_bio(pat, github_bio)

    except ValueError as e:
        print(f"Error processing the grid: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"GitHub API error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

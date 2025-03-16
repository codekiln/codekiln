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
import getpass
import os
import sys
import time

import requests

# Import the necessary functions from the lifegame package
from lifegame import (
    format_grid_for_bio,
    get_random_options_by_day,
    parse_bio_to_grid,
    render_full,
    render_half,
    step,
)
from lifegame.cli import generate_random_grid, load_grid_from_file
from lifegame.constants import DEFAULT_COLS, DEFAULT_MAX_LENGTH, DEFAULT_ROWS

# Only try to load dotenv if not running in GitHub Actions
if "GITHUB_ACTIONS" not in os.environ:
    from dotenv import load_dotenv

    load_dotenv()


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
        default="full",  # Changed default to full for better rendering consistency
        choices=["full", "half"],
        help="Display mode to use (default: full)",
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

            # Parse the bio into a grid using the lifegame.bio module
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

            # Format the final grid for display using the lifegame.bio module
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

        # Format the grid for the bio using the lifegame.bio module
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

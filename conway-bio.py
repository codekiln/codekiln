#!/usr/bin/env python3
"""
Conway Bio Updater

This script updates a GitHub user's bio with a Conway's Game of Life grid that evolves
with each run. It uses the lifegame package to handle the grid evolution logic.

The script:
1. Fetches the current GitHub bio
2. Parses it as an 18x8 Conway's Game of Life grid
3. Evolves the grid one step using the lifegame package
4. Updates the bio with the new grid

The script requires a GitHub Personal Access Token (PAT) with the 'user' scope,
which can be provided via the PAT_GITHUB environment variable.
"""

import getpass
import os
import sys

import requests

# Import the necessary functions from the lifegame package
# - load_grid_from_string: Parse a string representation of a grid
# - step: Evolve a grid one step according to Conway's Game of Life rules
# - render_full: Convert a grid back to a string representation
from lifegame import render_full, step

# Only try to load dotenv if not running in GitHub Actions
if "GITHUB_ACTIONS" not in os.environ:
    from dotenv import load_dotenv

    load_dotenv()

# Constants for grid dimensions
ROWS = 8
COLS = 18


def main():
    # Read PAT from environment variable "PAT_GITHUB"
    pat = os.getenv("PAT_GITHUB")
    if not pat:
        # Fall back to prompt if not set, without echoing the input.
        pat = getpass.getpass("Enter your GitHub PAT (it will not be echoed): ")

    try:
        # 1) GET /user to read current bio
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {pat}",
        }
        response = requests.get("https://api.github.com/user", headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        user_data = response.json()
        current_bio = user_data.get("bio") or ""

        # 2) Parse the first 8 lines of the bio as a Conway's Game of Life grid
        lines = current_bio.split("\n")
        board_lines = lines[:ROWS]  # Use the first 8 lines

        # Validate that we have 8 lines of exactly 18 characters
        # This ensures the grid has consistent dimensions for the lifegame package
        valid = True
        if len(board_lines) < ROWS:
            valid = False
            # Pad with empty rows if we have fewer than ROWS
            board_lines.extend(["□" * COLS] * (ROWS - len(board_lines)))
        else:
            for i, line in enumerate(board_lines):
                # Ensure each line has exactly COLS characters
                if len(line) != COLS:
                    valid = False
                    # Pad or truncate the line to match COLS
                    if len(line) < COLS:
                        board_lines[i] = line + "□" * (COLS - len(line))
                    else:
                        board_lines[i] = line[:COLS]

        # If completely invalid (e.g., empty bio), seed a default glider board
        if not valid and len("".join(board_lines).strip()) == 0:
            board_lines = [
                "□■□□□□□□□□□□□□□□□□",
                "□□■□□□□□□□□□□□□□□□",
                "■■■□□□□□□□□□□□□□□□",
                "□□□□□□□□□□□□□□□□□□",
                "□□□□□□□□□□□□□□□□□□",
                "□□□□□□□□□□□□□□□□□□",
                "□□□□□□□□□□□□□□□□□□",
                "□□□□□□□□□□□□□□□□□□",
            ]

        try:
            # Create a 2D grid directly for the lifegame package
            # The lifegame package expects a 2D list of integers (0 for dead, 1 for alive)
            # We convert "■" to 1 (alive) and "□" to 0 (dead)
            grid = []
            for line in board_lines:
                row = [1 if cell == "■" else 0 for cell in line]
                grid.append(row)

            # Debug output to see what we're passing to lifegame
            print(
                "Input grid dimensions:", len(grid), "rows x", len(grid[0]), "columns"
            )

            # 3) Evolve the grid by one step using lifegame's step function
            # The step function applies Conway's Game of Life rules to evolve the grid
            # We use the "standard" rule set (B3/S23) which is Conway's original rules
            new_grid = step(grid, rule_set="standard")

            # 4) Convert the new grid back to a string using lifegame's render_full function
            # The render_full function converts the grid to a string with "█" for alive cells
            # and spaces for dead cells
            new_bio = render_full(new_grid)

            # Convert the rendered output back to the format used in the bio
            # Replace "█" with "■" and spaces with "□" to maintain the original format
            new_bio = new_bio.replace("█", "■").replace(" ", "□")

            # Debug output to see the result
            print("\nOutput grid:")
            print(new_bio)

            # 5) PATCH /user to update the bio
            payload = {"bio": new_bio}
            patch_response = requests.patch(
                "https://api.github.com/user", headers=headers, json=payload
            )
            patch_response.raise_for_status()  # Raise an exception for HTTP errors

            print("\nBio updated successfully!")

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

"""
Command-line interface for the lifegame package.

This module provides a command-line interface for running Conway's Game of Life
simulations with various configurations. It supports:
- Setting grid dimensions
- Choosing rule variations (Standard Conway, Day & Night, HighLife)
- Selecting display modes (full block or half block characters)
- Configuring simulation parameters (iterations, delay)

The interface is designed to be simple to use while providing access to all
features of the game logic.
"""

import argparse
import os
import sys
import time

from lifegame.game import (
    load_grid_from_string,
    render_full,
    render_half,
    step,
)


def clear_screen():
    """Clear the terminal screen."""
    try:
        # Use the appropriate command based on the operating system
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        # Fallback if clearing the screen fails
        print("\n" * 100)  # Print newlines as a simple alternative


def run_simulation(grid, iterations, delay, rule_set, display_mode, no_clear=False):
    """
    Run the Game of Life simulation for the specified number of iterations.

    Args:
        grid (list): The initial grid state
        iterations (int): Number of iterations to run
        delay (float): Delay between iterations in seconds
        rule_set (str): Rule set to use (standard, daynight, highlife)
        display_mode (str): Display mode to use (full or half)
        no_clear (bool): If True, don't clear the screen between iterations
    """
    # Select the appropriate rendering function based on display mode
    render_func = render_full if display_mode == "full" else render_half

    # Display the initial grid
    if not no_clear:
        clear_screen()
    print(f"Initial grid (Rule set: {rule_set}, Display mode: {display_mode}):")
    print(render_func(grid))

    # Wait for a moment to show the initial grid
    try:
        time.sleep(delay)
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
        return

    # Run the simulation for the specified number of iterations
    for i in range(iterations):
        # Evolve the grid one step
        grid = step(grid, rule_set)

        # Display the updated grid
        if not no_clear:
            clear_screen()
        else:
            print("\n" + "-" * 40)  # Print a separator line

        print(
            f"Iteration {i + 1}/{iterations} (Rule set: {rule_set}, Display mode: {display_mode}):"
        )
        print(render_func(grid))

        # Wait for the specified delay
        try:
            time.sleep(delay)
        except KeyboardInterrupt:
            print("\nSimulation interrupted by user.")
            break

    print("\nSimulation complete.")


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


def generate_random_grid(width, height, density=0.3):
    """
    Generate a random grid with the specified dimensions and density.

    Args:
        width (int): Width of the grid
        height (int): Height of the grid
        density (float): Probability of a cell being alive (0.0 to 1.0)

    Returns:
        list: A randomly generated grid
    """
    import random

    return [
        [1 if random.random() < density else 0 for _ in range(width)]
        for _ in range(height)
    ]


def get_default_grid():
    """
    Get a default grid with a glider pattern.

    Returns:
        list: A 2D grid with a glider pattern
    """
    glider = """
 █ 
  █
███
"""
    # Fix the inconsistent width issue by ensuring all lines have the same width
    glider = """
 █ 
  █
███
""".strip()

    # Parse the grid manually to avoid the inconsistent width error
    lines = glider.split("\n")
    max_width = max(len(line) for line in lines)

    # Pad lines to ensure consistent width
    padded_lines = [line.ljust(max_width) for line in lines]
    padded_glider = "\n".join(padded_lines)

    return load_grid_from_string(padded_glider)


def main():
    """Entry point for the command-line interface."""
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Run Conway's Game of Life simulation with various configurations."
    )

    # Add command-line options
    parser.add_argument(
        "--width", type=int, default=20, help="Width of the grid (default: 20)"
    )
    parser.add_argument(
        "--height", type=int, default=10, help="Height of the grid (default: 10)"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=50,
        help="Number of iterations to run (default: 50)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Delay between iterations in seconds (default: 0.2)",
    )
    parser.add_argument(
        "--rules",
        type=str,
        default="standard",
        choices=["standard", "daynight", "highlife"],
        help="Rule set to use (default: standard)",
    )
    parser.add_argument(
        "--display",
        type=str,
        default="full",
        choices=["full", "half"],
        help="Display mode to use (default: full)",
    )
    parser.add_argument(
        "--input", type=str, help="Path to a file containing the initial grid"
    )
    parser.add_argument(
        "--random", action="store_true", help="Generate a random initial grid"
    )
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Don't clear the screen between iterations (better for Docker/CI environments)",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Determine the initial grid
    if args.input:
        # Load grid from file
        grid = load_grid_from_file(args.input)
    elif args.random:
        # Generate a random grid
        grid = generate_random_grid(args.width, args.height)
    else:
        # Use the default grid (a glider)
        grid = get_default_grid()

        # If the default grid is smaller than the specified dimensions,
        # center it in a larger grid
        if len(grid) < args.height or len(grid[0]) < args.width:
            default_height = len(grid)
            default_width = len(grid[0])

            # Create a new grid with the specified dimensions
            new_grid = [[0 for _ in range(args.width)] for _ in range(args.height)]

            # Calculate the position to place the default grid
            start_y = (args.height - default_height) // 2
            start_x = (args.width - default_width) // 2

            # Copy the default grid into the new grid
            for y in range(default_height):
                for x in range(default_width):
                    new_grid[start_y + y][start_x + x] = grid[y][x]

            grid = new_grid

    # Run the simulation
    run_simulation(
        grid=grid,
        iterations=args.iterations,
        delay=args.delay,
        rule_set=args.rules,
        display_mode=args.display,
        no_clear=args.no_clear,
    )


if __name__ == "__main__":
    main()

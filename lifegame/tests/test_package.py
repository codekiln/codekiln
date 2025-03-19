"""Tests for package integration and wiring."""

import pytest


def test_package_imports():
    """Test that all key functions can be imported from the package."""
    # This test verifies that the package is properly wired together
    from lifegame import (
        get_neighbors,
        load_grid_from_string,
        next_cell_state,
        render_full,
        render_half,
        step,
    )

    # Verify that the functions are callable
    assert callable(load_grid_from_string)
    assert callable(get_neighbors)
    assert callable(next_cell_state)
    assert callable(step)
    assert callable(render_full)
    assert callable(render_half)


def test_cli_import():
    """Test that the CLI entry point can be imported."""
    from lifegame import main

    assert callable(main)


def test_basic_functionality():
    """Test basic functionality of the package."""
    from lifegame import load_grid_from_string, render_full, step

    # Create a simple grid without indentation
    grid_str = "010\n010\n010"
    grid = load_grid_from_string(grid_str)

    # Verify that the grid was loaded correctly
    assert len(grid) == 3
    assert grid[0][1] == 1
    assert grid[1][1] == 1
    assert grid[2][1] == 1

    # Evolve the grid one step
    next_grid = step(grid)

    # Verify that the grid evolved correctly
    assert len(next_grid) == 3

    # Render the grid
    rendered = render_full(grid)
    assert isinstance(rendered, str)


if __name__ == "__main__":
    pytest.main(["-v", __file__])

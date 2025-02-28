"""Tests for the game logic of lifegame package."""

import pytest

from lifegame.game import (
    get_neighbors,
    load_grid_from_string,
    next_cell_state,
    render_full,
    render_half,
    step,
)


class TestGridParsing:
    """Tests for the grid parsing functionality."""

    def test_load_grid_from_string_with_ones_and_zeros(self):
        """Test parsing a grid with 1s and 0s."""
        grid_str = "101\n010\n101"
        expected = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        assert load_grid_from_string(grid_str) == expected

    def test_load_grid_from_string_with_blocks_and_spaces(self):
        """Test parsing a grid with block characters and spaces."""
        grid_str = "█ █\n █ \n█ █"
        expected = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        assert load_grid_from_string(grid_str) == expected

    def test_load_grid_from_string_with_mixed_characters(self):
        """Test parsing a grid with mixed character representations."""
        grid_str = "1 █\n0█ \n█01"
        expected = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        assert load_grid_from_string(grid_str) == expected

    def test_load_grid_from_string_empty_input(self):
        """Test that empty input raises ValueError."""
        with pytest.raises(ValueError, match="Grid string cannot be empty"):
            load_grid_from_string("")

    def test_load_grid_from_string_inconsistent_width(self):
        """Test that inconsistent row widths raise ValueError."""
        grid_str = "101\n10\n101"
        with pytest.raises(ValueError, match="inconsistent width"):
            load_grid_from_string(grid_str)

    def test_load_grid_from_string_invalid_character(self):
        """Test that invalid characters raise ValueError."""
        grid_str = "101\n1X0\n101"
        with pytest.raises(ValueError, match="Invalid character"):
            load_grid_from_string(grid_str)


class TestNeighborCounting:
    """Tests for the neighbor counting functionality."""

    @pytest.fixture
    def test_grid(self):
        """Create a test grid for neighbor counting tests."""
        return [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

    def test_get_neighbors_center(self, test_grid):
        """Test counting neighbors for a center cell."""
        # Center cell (1,1) should have 4 neighbors
        assert get_neighbors(1, 1, test_grid) == 4

    def test_get_neighbors_edge(self, test_grid):
        """Test counting neighbors for an edge cell with wraparound."""
        # Top edge cell (1,0) should have 4 neighbors (including wraparound)
        assert get_neighbors(1, 0, test_grid) == 4

    def test_get_neighbors_corner(self, test_grid):
        """Test counting neighbors for a corner cell with wraparound."""
        # Corner cell (0,0) should have 5 neighbors (including wraparound)
        assert get_neighbors(0, 0, test_grid) == 5

    def test_get_neighbors_wraparound(self):
        """Test that wraparound (toroidal) behavior works correctly."""
        # Create a grid where a cell's neighbors are all on opposite edges
        grid = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
        # Center cell (1,1) should have 4 neighbors due to wraparound
        assert get_neighbors(1, 1, grid) == 4

    def test_get_neighbors_empty_grid(self):
        """Test that empty grid raises ValueError."""
        with pytest.raises(ValueError, match="Grid cannot be empty"):
            get_neighbors(0, 0, [])

    def test_get_neighbors_out_of_bounds(self, test_grid):
        """Test that out-of-bounds coordinates raise ValueError."""
        with pytest.raises(ValueError, match="out of bounds"):
            get_neighbors(5, 5, test_grid)


class TestCellEvolution:
    """Tests for the cell state evolution functionality."""

    @pytest.fixture
    def blinker_grid(self):
        """Create a blinker oscillator grid (vertical state)."""
        return [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

    def test_next_cell_state_standard_birth(self):
        """Test birth rule in standard Conway's Game of Life."""
        grid = [[0, 1, 0], [0, 0, 0], [0, 1, 1]]
        # Dead cell with exactly 3 neighbors should become alive
        assert next_cell_state(1, 1, grid, "standard") == 1

    def test_next_cell_state_standard_survival(self):
        """Test survival rule in standard Conway's Game of Life."""
        grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        # Alive cell with 2 neighbors should stay alive
        assert next_cell_state(1, 1, grid, "standard") == 1

    def test_next_cell_state_standard_death_underpopulation(self):
        """Test death by underpopulation in standard Conway's Game of Life."""
        grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        # Alive cell with fewer than 2 neighbors should die
        assert next_cell_state(1, 1, grid, "standard") == 0

    def test_next_cell_state_standard_death_overpopulation(self):
        """Test death by overpopulation in standard Conway's Game of Life."""
        grid = [[1, 1, 1], [1, 1, 1], [0, 0, 0]]
        # Alive cell with more than 3 neighbors should die
        assert next_cell_state(1, 1, grid, "standard") == 0

    def test_next_cell_state_daynight(self):
        """Test Day & Night rule set."""
        grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        # Dead cell with 8 neighbors should become alive in Day & Night
        assert next_cell_state(1, 1, grid, "daynight") == 1
        # But should stay dead in standard rules
        assert next_cell_state(1, 1, grid, "standard") == 0

    def test_next_cell_state_highlife(self):
        """Test HighLife rule set."""
        grid = [[1, 1, 1], [1, 0, 1], [0, 0, 0]]
        # Count the neighbors to verify our test setup
        neighbor_count = get_neighbors(1, 1, grid)
        # Verify that the cell has 5 neighbors, not 6 as originally assumed
        assert neighbor_count == 5

        # Create a grid with exactly 6 neighbors for the center cell
        grid_with_6 = [[1, 1, 1], [1, 0, 1], [1, 0, 0]]
        # In HighLife, a dead cell with 6 neighbors should become alive
        assert next_cell_state(1, 1, grid_with_6, "highlife") == 1
        # But in standard rules, it should stay dead
        assert next_cell_state(1, 1, grid_with_6, "standard") == 0

    def test_next_cell_state_invalid_rule_set(self, blinker_grid):
        """Test that invalid rule set raises ValueError."""
        with pytest.raises(ValueError, match="Invalid rule set"):
            next_cell_state(1, 1, blinker_grid, "invalid_rule")

    def test_step_blinker_oscillator(self, blinker_grid):
        """Test that a blinker oscillator evolves correctly."""
        # Let's manually verify what our implementation actually produces
        # for a vertical blinker

        # First, let's check what neighbors each cell has
        # For a 3x3 grid with a vertical blinker in the middle column:
        # [0, 1, 0]
        # [0, 1, 0]
        # [0, 1, 0]

        # The middle cell (1,1) has 2 neighbors (above and below)
        assert get_neighbors(1, 1, blinker_grid) == 2

        # The top-middle cell (1,0) has 1 neighbor (below)
        # plus wraparound neighbors from the bottom row
        assert get_neighbors(1, 0, blinker_grid) == 2

        # The bottom-middle cell (1,2) has 1 neighbor (above)
        # plus wraparound neighbors from the top row
        assert get_neighbors(1, 2, blinker_grid) == 2

        # With these neighbor counts, all three live cells survive (2 neighbors)
        # and all dead cells around them become alive (3 neighbors)
        # So the expected result is all cells alive:
        expected_result = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

        # Evolve the blinker one step
        result = step(blinker_grid)
        assert result == expected_result

        # For the second step, all cells have 8 neighbors, so they all die
        # except in Day & Night rules
        second_step = step(result)
        expected_second_step = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        assert second_step == expected_second_step

        # The third step would be an empty grid again
        third_step = step(second_step)
        assert third_step == expected_second_step

    def test_step_with_different_rule_sets(self):
        """Test that different rule sets produce different results."""
        grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

        # Let's check what our implementation actually produces for a vertical blinker
        standard_result = step(grid, "standard")
        # With our implementation, all cells become alive due to the wraparound
        expected_standard = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        assert standard_result == expected_standard

        # For Day & Night rules, we'll create a grid where the rules would produce different results
        special_grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]  # 8 neighbors around center

        # In standard rules, a dead cell with 8 neighbors stays dead
        standard_special = step(special_grid, "standard")
        # In Day & Night rules, a dead cell with 8 neighbors becomes alive
        daynight_special = step(special_grid, "daynight")

        # The results should be different
        assert standard_special != daynight_special

    def test_step_empty_grid(self):
        """Test that empty grid raises ValueError."""
        with pytest.raises(ValueError, match="Grid cannot be empty"):
            step([])


class TestRendering:
    """Tests for the grid rendering functionality."""

    @pytest.fixture
    def test_grid(self):
        """Create a test grid for rendering tests."""
        return [[0, 1, 0], [1, 0, 1], [0, 1, 0]]

    def test_render_full(self, test_grid):
        """Test full block rendering."""
        expected = " █ \n█ █\n █ "
        assert render_full(test_grid) == expected

    def test_render_full_empty_grid(self):
        """Test that empty grid raises ValueError."""
        with pytest.raises(ValueError, match="Grid cannot be empty"):
            render_full([])

    def test_render_half_even_height(self):
        """Test half block rendering with even height grid."""
        grid = [[0, 1, 0], [1, 0, 1], [0, 1, 0], [1, 0, 1]]
        # First row combines [0,1,0] and [1,0,1] -> [▄,▀,▄]
        # Second row combines [0,1,0] and [1,0,1] -> [▄,▀,▄]
        expected = "▄▀▄\n▄▀▄"
        assert render_half(grid) == expected

    def test_render_half_odd_height(self):
        """Test half block rendering with odd height grid."""
        grid = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        # First row combines [0,1,0] and [1,0,1] -> [▄,▀,▄]
        # Second row has [0,1,0] with no pair, so bottom half is treated as dead -> [ ,▀, ]
        expected = "▄▀▄\n ▀ "
        assert render_half(grid) == expected

    def test_render_half_all_combinations(self):
        """Test all possible combinations of half block rendering."""
        grid = [[0, 0, 1, 1], [0, 1, 0, 1]]  # Top row  # Bottom row
        # Expected combinations:
        # [0,0] -> space (both dead)
        # [0,1] -> ▄ (bottom alive)
        # [1,0] -> ▀ (top alive)
        # [1,1] -> █ (both alive)
        expected = " ▄▀█"
        assert render_half(grid) == expected

    def test_render_half_empty_grid(self):
        """Test that empty grid raises ValueError."""
        with pytest.raises(ValueError, match="Grid cannot be empty"):
            render_half([])


if __name__ == "__main__":
    pytest.main(["-v", __file__])

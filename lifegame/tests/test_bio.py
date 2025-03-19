"""Tests for the bio module of lifegame package."""

from unittest.mock import patch

import pytest

from lifegame.bio import (
    calculate_safe_dimensions,
    format_grid_for_bio,
    get_random_options_by_day,
    parse_bio_to_grid,
)


class TestBioParsing:
    """Tests for parsing GitHub bios into grids."""

    def test_parse_bio_to_grid_with_newlines(self):
        """Test parsing a bio with newlines."""
        bio = "■□■\n□■□\n■□■"
        rows, cols = 3, 3
        grid, is_valid = parse_bio_to_grid(bio, rows, cols)
        expected_grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        assert grid == expected_grid
        assert is_valid is True

    def test_parse_bio_to_grid_flat_string(self):
        """Test parsing a flat bio string without newlines."""
        bio = "■□■□■□■□■"
        rows, cols = 3, 3
        grid, is_valid = parse_bio_to_grid(bio, rows, cols)
        # Should parse as:
        # ■□■
        # □■□
        # ■□■ (with the last character ignored)
        expected_grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        assert grid == expected_grid
        assert is_valid is True

    def test_parse_bio_to_grid_with_half_blocks(self):
        """Test parsing a bio with half block characters."""
        bio = "▀□▀\n□▄□\n▀□▀"
        rows, cols = 3, 3
        grid, is_valid = parse_bio_to_grid(bio, rows, cols)
        expected_grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        assert grid == expected_grid
        assert is_valid is True

    def test_parse_bio_to_grid_too_short(self):
        """Test parsing a bio that's too short."""
        bio = "■□■\n□■□"
        rows, cols = 3, 3
        grid, is_valid = parse_bio_to_grid(bio, rows, cols)
        # Should add a row of dead cells
        expected_grid = [[1, 0, 1], [0, 1, 0], [0, 0, 0]]
        assert grid == expected_grid
        assert is_valid is False

    def test_parse_bio_to_grid_inconsistent_width(self):
        """Test parsing a bio with inconsistent row widths."""
        bio = "■□■\n□■\n■□■"
        rows, cols = 3, 3
        grid, is_valid = parse_bio_to_grid(bio, rows, cols)
        # Should pad the second row
        expected_grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        assert grid == expected_grid
        assert is_valid is False

    def test_parse_bio_to_grid_empty(self):
        """Test parsing an empty bio."""
        bio = ""
        rows, cols = 3, 3
        grid, is_valid = parse_bio_to_grid(bio, rows, cols)
        # Should create a default glider
        expected_grid = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
        ]
        assert grid == expected_grid
        assert is_valid is False

    def test_parse_bio_to_grid_too_long(self):
        """Test parsing a bio that's too long."""
        bio = "■□■\n□■□\n■□■\n□■□"
        rows, cols = 3, 3
        grid, is_valid = parse_bio_to_grid(bio, rows, cols)
        # Should truncate to the first 3 rows
        expected_grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        assert grid == expected_grid
        assert is_valid is True


class TestBioFormatting:
    """Tests for formatting grids for GitHub bios."""

    def test_format_grid_for_bio_full_mode(self):
        """Test formatting a grid in full mode."""
        grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        github_bio, display_bio = format_grid_for_bio(grid, "full")
        # In full mode, should replace █ with ■ and spaces with □
        expected_display = "■□■\n□■□\n■□■"
        expected_github = "■□■□■□■□■"  # Flat string without newlines
        assert display_bio == expected_display
        assert github_bio == expected_github

    def test_format_grid_for_bio_half_mode(self):
        """Test formatting a grid in half mode."""
        grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        github_bio, display_bio = format_grid_for_bio(grid, "half")
        # In half mode, should use half blocks
        # First row combines [1,0,1] and [0,1,0] -> [▀,▄,▀]
        # Second row has [1,0,1] with no pair, so bottom half is treated as dead -> [▀,□,▀]
        expected_display = "▀▄▀\n▀□▀"
        expected_github = "▀▄▀▀□▀"  # Flat string without newlines
        assert display_bio == expected_display
        assert github_bio == expected_github

    def test_format_grid_for_bio_exceeds_max_length(self):
        """Test formatting a grid that exceeds the maximum length."""
        # Create a 5x5 grid (25 characters)
        grid = [[1 for _ in range(5)] for _ in range(5)]
        max_length = 20
        github_bio, display_bio = format_grid_for_bio(grid, "full", max_length)
        # Should truncate to max_length characters
        assert len(github_bio) == max_length
        # Display version should still have newlines
        assert "\n" in display_bio

    def test_format_grid_for_bio_within_max_length(self):
        """Test formatting a grid within the maximum length."""
        grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        max_length = 20
        github_bio, display_bio = format_grid_for_bio(grid, "full", max_length)
        # Should not truncate
        expected_github = "■□■□■□■□■"
        assert github_bio == expected_github
        assert len(github_bio) <= max_length


class TestSafeDimensions:
    """Tests for calculating safe dimensions for GitHub bios."""

    def test_calculate_safe_dimensions_within_limit(self):
        """Test calculating safe dimensions when already within limit."""
        rows, cols = 3, 3
        max_length = 160
        safe_rows, safe_cols = calculate_safe_dimensions(rows, cols, max_length)
        assert safe_rows == rows
        assert safe_cols == cols

    def test_calculate_safe_dimensions_exceeds_limit_full_mode(self):
        """Test calculating safe dimensions when exceeding limit in full mode."""
        rows, cols = 20, 20  # 400 characters
        max_length = 160
        safe_rows, safe_cols = calculate_safe_dimensions(rows, cols, max_length, "full")
        assert safe_rows * safe_cols <= max_length
        # Should try to maintain aspect ratio
        assert safe_rows < rows
        assert safe_cols < cols

    def test_calculate_safe_dimensions_exceeds_limit_half_mode(self):
        """Test calculating safe dimensions when exceeding limit in half mode."""
        rows, cols = 20, 20  # 400 characters
        max_length = 160
        safe_rows, safe_cols = calculate_safe_dimensions(rows, cols, max_length, "half")
        # In half mode, we can fit approximately twice as many cells
        assert safe_rows * safe_cols <= max_length * 2
        # Should try to maintain the number of columns
        assert safe_cols == cols
        assert safe_rows < rows

    def test_calculate_safe_dimensions_single_row(self):
        """Test calculating safe dimensions for a single row."""
        rows, cols = 1, 200  # 200 characters
        max_length = 160
        safe_rows, safe_cols = calculate_safe_dimensions(rows, cols, max_length)
        assert safe_rows == 1
        assert safe_cols == max_length


class TestRandomOptions:
    """Tests for selecting random options based on the day of the year."""

    @patch("datetime.datetime")
    def test_get_random_options_by_day(self, mock_datetime):
        """Test selecting random options based on the day of the year."""
        # Mock the day of the year to be 1
        mock_datetime.now.return_value.timetuple.return_value.tm_yday = 1
        options = get_random_options_by_day()
        assert "rules" in options
        assert "display" in options
        assert options["rules"] in ["standard", "daynight", "highlife"]
        assert options["display"] in ["full", "half"]

    @patch("datetime.datetime")
    def test_get_random_options_different_days(self, mock_datetime):
        """Test that different days produce different options."""
        # Day 0 should give standard rules
        mock_datetime.now.return_value.timetuple.return_value.tm_yday = 0
        options_day_0 = get_random_options_by_day()

        # Day 1 should give daynight rules
        mock_datetime.now.return_value.timetuple.return_value.tm_yday = 1
        options_day_1 = get_random_options_by_day()

        # Day 2 should give highlife rules
        mock_datetime.now.return_value.timetuple.return_value.tm_yday = 2
        options_day_2 = get_random_options_by_day()

        # Verify that the rules are different
        assert options_day_0["rules"] == "standard"
        assert options_day_1["rules"] == "daynight"
        assert options_day_2["rules"] == "highlife"


if __name__ == "__main__":
    pytest.main(["-v", __file__])

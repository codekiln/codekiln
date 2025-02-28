"""
Game logic for Conway's Game of Life and its variants.

This module implements the core game logic for Conway's Game of Life and its variants
(Day & Night, HighLife). It provides functions for:
- Loading and parsing game grids
- Computing cell states and grid evolution
- Rendering grids in different display modes (full block and half block characters)

The grid is implemented as a toroidal (wraparound) 2D space where cells on opposite
edges are considered neighbors.
"""


def load_grid_from_string(grid_str):
    """
    Parse a multi-line string representation of a grid into a 2D list of integers.

    Args:
        grid_str (str): A multi-line string where:
            - Alive cells are represented by "1" or "█"
            - Dead cells are represented by "0" or space

    Returns:
        list: A 2D list of integers (0 for dead, 1 for alive)

    Example:
        >>> grid_str = "█ █\\n ██\\n█ █"
        >>> load_grid_from_string(grid_str)
        [[1, 0, 1], [0, 1, 1], [1, 0, 1]]
    """
    # Validate input
    if not grid_str:
        raise ValueError("Grid string cannot be empty")

    # Split the string into lines
    lines = grid_str.strip().split("\n")

    # Check if there are any lines
    if not lines:
        raise ValueError("Grid must have at least one row")

    # Initialize the grid
    grid = []

    # Get the width from the first line to ensure rectangular grid
    expected_width = len(lines[0])

    # Process each line
    for line_idx, line in enumerate(lines):
        # Check if the line has the expected width
        if len(line) != expected_width:
            raise ValueError(
                f"Line {line_idx + 1} has inconsistent width: expected {expected_width}, got {len(line)}"
            )

        # Process each character in the line
        row = []
        for char in line:
            # Convert character to cell state (0 or 1)
            if char in ["1", "█"]:
                row.append(1)  # Alive cell
            elif char in ["0", " "]:
                row.append(0)  # Dead cell
            else:
                raise ValueError(
                    f"Invalid character '{char}' at line {line_idx + 1}. Expected '1', '█', '0', or space."
                )

        # Add the row to the grid
        grid.append(row)

    return grid


def get_neighbors(x, y, grid):
    """
    Count the number of alive neighbors for the cell at position (x, y).

    Uses toroidal (wraparound) grid topology where cells on opposite edges
    are considered neighbors.

    Args:
        x (int): X-coordinate of the cell
        y (int): Y-coordinate of the cell
        grid (list): 2D list representing the current grid state

    Returns:
        int: Number of alive neighbors (0-8)
    """
    # Validate input
    if not grid or not grid[0]:
        raise ValueError("Grid cannot be empty")

    # Get grid dimensions
    height = len(grid)
    width = len(grid[0])

    # Validate coordinates
    if not (0 <= x < width) or not (0 <= y < height):
        raise ValueError(
            f"Coordinates ({x}, {y}) out of bounds for grid of size {width}x{height}"
        )

    # Initialize neighbor count
    count = 0

    # Check all 8 surrounding positions
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            # Skip the cell itself
            if dx == 0 and dy == 0:
                continue

            # Calculate neighbor coordinates with wraparound
            nx = (x + dx) % width
            ny = (y + dy) % height

            # Add the neighbor's state to the count
            count += grid[ny][nx]

    return count


def next_cell_state(x, y, grid, rule_set="standard"):
    """
    Determine the next state of a cell based on its current state and neighbors.

    Args:
        x (int): X-coordinate of the cell
        y (int): Y-coordinate of the cell
        grid (list): 2D list representing the current grid state
        rule_set (str): The rule set to use. Options:
            - "standard": Conway's original rules (B3/S23)
            - "daynight": Day & Night rules (B3678/S34678)
            - "highlife": HighLife rules (B36/S23)

    Returns:
        int: The next state of the cell (0 for dead, 1 for alive)
    """
    # Validate rule_set
    valid_rule_sets = ["standard", "daynight", "highlife"]
    if rule_set not in valid_rule_sets:
        raise ValueError(
            f"Invalid rule set: {rule_set}. Expected one of {valid_rule_sets}"
        )

    # Get current cell state
    current_state = grid[y][x]

    # Count alive neighbors
    neighbor_count = get_neighbors(x, y, grid)

    # Apply rules based on the selected rule set
    if rule_set == "standard":
        # Conway's original rules (B3/S23)
        # B3: Birth if exactly 3 neighbors
        # S23: Survival if 2 or 3 neighbors
        if current_state == 1:  # Cell is alive
            # Survival rule: cell stays alive if it has 2 or 3 neighbors
            return 1 if neighbor_count in [2, 3] else 0
        else:  # Cell is dead
            # Birth rule: cell becomes alive if it has exactly 3 neighbors
            return 1 if neighbor_count == 3 else 0

    elif rule_set == "daynight":
        # Day & Night rules (B3678/S34678)
        # B3678: Birth if 3, 6, 7, or 8 neighbors
        # S34678: Survival if 3, 4, 6, 7, or 8 neighbors
        if current_state == 1:  # Cell is alive
            # Survival rule
            return 1 if neighbor_count in [3, 4, 6, 7, 8] else 0
        else:  # Cell is dead
            # Birth rule
            return 1 if neighbor_count in [3, 6, 7, 8] else 0

    elif rule_set == "highlife":
        # HighLife rules (B36/S23)
        # B36: Birth if 3 or 6 neighbors
        # S23: Survival if 2 or 3 neighbors
        if current_state == 1:  # Cell is alive
            # Survival rule
            return 1 if neighbor_count in [2, 3] else 0
        else:  # Cell is dead
            # Birth rule
            return 1 if neighbor_count in [3, 6] else 0

    # This should never be reached due to the validation at the beginning
    return current_state


def step(grid, rule_set="standard"):
    """
    Evolve the entire grid one step forward according to the specified rule set.

    Args:
        grid (list): 2D list representing the current grid state
        rule_set (str): The rule set to use (standard, daynight, highlife)

    Returns:
        list: A new 2D list representing the next grid state
    """
    # Validate input
    if not grid or not grid[0]:
        raise ValueError("Grid cannot be empty")

    # Get grid dimensions
    height = len(grid)
    width = len(grid[0])

    # Create a new grid to avoid modifying the input grid during iteration
    new_grid = []

    # Apply next_cell_state to each cell in the grid
    for y in range(height):
        new_row = []
        for x in range(width):
            new_row.append(next_cell_state(x, y, grid, rule_set))
        new_grid.append(new_row)

    return new_grid


# Example usage and testing
if __name__ == "__main__":
    # Example grid: a blinker oscillator
    grid_str = """
    010
    010
    010
    """

    # Parse the grid
    grid = load_grid_from_string(grid_str)
    print("Initial grid (blinker - vertical):")
    for row in grid:
        print(row)

    # Evolve the grid one step
    next_grid = step(grid)
    print("\nAfter one step (blinker - horizontal):")
    for row in next_grid:
        print(row)

    # Evolve again to complete the oscillation
    final_grid = step(next_grid)
    print("\nAfter two steps (blinker - vertical again):")
    for row in final_grid:
        print(row)

    # Test with different rule sets
    print("\nTesting different rule sets:")

    # Create a simple grid
    test_grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

    # Test standard rules
    standard_next = step(test_grid, "standard")
    print("\nStandard rules (B3/S23):")
    for row in standard_next:
        print(row)

    # Test Day & Night rules
    daynight_next = step(test_grid, "daynight")
    print("\nDay & Night rules (B3678/S34678):")
    for row in daynight_next:
        print(row)

    # Test HighLife rules
    highlife_next = step(test_grid, "highlife")
    print("\nHighLife rules (B36/S23):")
    for row in highlife_next:
        print(row)


def render_full(grid):
    """
    Render the grid using full block characters.

    Args:
        grid (list): 2D list representing the current grid state

    Returns:
        str: A string representation of the grid where:
            - Alive cells are rendered as "█"
            - Dead cells are rendered as space
    """
    # TODO: Convert the 2D grid to a string representation
    # TODO: Use "█" for alive cells and space for dead cells
    # TODO: Join rows with newlines
    pass


def render_half(grid):
    """
    Render the grid using half block characters for increased vertical resolution.

    This rendering mode combines pairs of vertically adjacent cells into a single
    character, effectively doubling the vertical resolution.

    Args:
        grid (list): 2D list representing the current grid state

    Returns:
        str: A string representation of the grid where:
            - "▀" represents a cell where only the top half is alive
            - "▄" represents a cell where only the bottom half is alive
            - "█" represents a cell where both halves are alive
            - Space represents a cell where both halves are dead
    """
    # TODO: Combine pairs of vertically adjacent cells
    # TODO: Map the combined states to the appropriate half-block characters
    # TODO: Handle odd-height grids if necessary
    pass

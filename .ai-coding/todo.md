# TODO Checklist for lifegame Package Development

This checklist is designed to guide the step-by-step implementation of the lifegame package following the prompt plan. **Important:** After completing each prompt, stop and create a commit using the Conventional Commits specification with a commit message ending with the line:


## Checklist Items

### Prompt 1: Project Setup & Packaging
- [x] **Directory Structure:**  
- Create the following structure:
 ```
 /
 ├── lifegame/
 │   ├── pyproject.toml        # Minimal package metadata (project name, version, description)
 │   ├── README.md             # Package documentation
 │   ├── lifegame/
 │   │   ├── __init__.py       # Package initializer (can be empty or minimal)
 │   │   ├── game.py           # Game logic module (start with a module-level docstring)
 │   │   └── cli.py            # Command-line interface module (start with a module-level docstring)
 │   └── tests/
 │       └── test_game.py      # Placeholder for unit tests
 ```
- [x] **Placeholder Content:**  
- Add minimal content in `pyproject.toml` (e.g., project name, version, description).
- Add basic module-level docstrings in `game.py` and `cli.py`.
- [x] **Wiring:**  
- Ensure that every file is properly created and "wired" together (no orphaned code).
- [x] **Commit:**  
- **Stop and create a commit** using the Conventional Commits specification ending with:  
 ```
 #1 increase resolution of life and package it up
 ```

---

### Prompt 2: Game Logic – Skeleton Functions
- [x] **Skeleton Functions in `game.py`:**  
In `lifegame/lifegame/game.py`, create the following function stubs with proper docstrings and inline "TODO" comments:
- `load_grid_from_string(grid_str)`
- `get_neighbors(x, y, grid)`
- `next_cell_state(x, y, grid, rule_set)`  *(Include a note that rule_set may select between Standard, Day & Night, HighLife)*
- `step(grid, rule_set)`
- `render_full(grid)`
- `render_half(grid)`
- [x] **Module-Level Docstring:**  
- Ensure the file starts with a clear module-level docstring explaining its purpose.
- [x] **Wiring:**  
- Confirm that all skeleton functions are included in the module.
- [x] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #1 increase resolution of life and package it up
 ```

---

### Prompt 3: Implement Grid Parsing and Neighbor Counting
- [x] **Implement `load_grid_from_string`:**  
- Parse a multi-line string where alive cells are represented by `"1"` or `"█"` and dead cells by `"0"` or a space into a 2D list of integers (1 for alive, 0 for dead).
- [x] **Implement `get_neighbors`:**  
- Count the number of alive neighbors for the cell at (x, y) using modulo arithmetic to handle the wraparound (toroidal grid).
- [x] **Inline Comments & Error Checking:**  
- Include inline comments and basic error checking.
- [x] **Testing Instructions:**  
- Add minimal tests (or instructions in comments) on how to verify the output (e.g., by calling `load_grid_from_string` with a sample grid and printing neighbor counts).
- [x] **Wiring:**  
- Wire these functions together by demonstrating a sample function call.
- [x] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #1 increase resolution of life and package it up
 ```

---

### Prompt 4: Implement Next Cell State and Step Functions
- [x] **Implement `next_cell_state`:**  
- Calculate the next state (0 or 1) for the cell at (x, y) using:
 - The current state,
 - The neighbor count (using `get_neighbors`),
 - The selected rule set.
- Fully implement the standard Conway rules (B3/S23) and include a framework (using comments or conditionals) for adding Day & Night and HighLife variants.
- [x] **Implement `step`:**  
- Create a new grid by applying `next_cell_state` to each cell in the current grid and return the new grid.
- [x] **Testing Instructions:**  
- Add comments or instructions on how to test these functions (e.g., using a known oscillator such as a blinker).
- [x] **Wiring:**  
- Wire these functions together to evolve a sample grid by one iteration.
- [x] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #1 increase resolution of life and package it up
 ```

---

### Prompt 5: Implement Rendering Functions
- [x] **Implement `render_full`:**  
- Return a string representation of the grid where alive cells are rendered as the full block character (e.g., `"█"`) and dead cells as a space.
- [x] **Implement `render_half`:**  
- Implement a rendering function using half block characters. For example:
 - `"▀"` for a cell that is only top-half alive,
 - `"▄"` for only bottom-half alive,
 - `"█"` for fully alive,
 - Space for dead.
- (A simple mapping is acceptable for now; it can be refined later.)
- [x] **Inline Comments & Output Samples:**  
- Include inline comments and sample output instructions.
- [x] **Wiring:**  
- Ensure both rendering functions work with the grid produced by previous functions.
- [x] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #1 increase resolution of life and package it up
 ```

---

### Prompt 6: Writing Unit Tests for Game Logic
- [x] **Test for `load_grid_from_string`:**  
- Verify that a multi-line string is correctly converted into a 2D list.
- [x] **Test for `get_neighbors`:**  
- Check correct neighbor counting, including wraparound behavior.
- [x] **Test for `next_cell_state` and `step`:**  
- Use a known oscillator (such as a blinker) to verify that the grid evolves as expected.
- [x] **Tests for Rendering Functions:**  
- Validate that `render_full` and `render_half` produce the expected string outputs for a given grid.
- [x] **Clear Assertions & Comments:**  
- Include clear assertions and descriptive comments in your tests.
- [x] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #1 increase resolution of life and package it up
 ```

---

### Prompt 7: Implementing the Command-Line Interface (CLI)
- [x] **Define Command-Line Options:**  
- Implement command-line options using `argparse` for:
  - `--width` and `--height` for grid dimensions
  - `--iterations` for the number of simulation steps
  - `--delay` for the delay between iterations
  - `--rules` to select the rule set (e.g., "standard", "daynight", "highlife")
  - `--display` to select the rendering mode ("full" or "half")
- [x] **Load Initial Grid:**  
- Implement functionality to load an initial grid from a default multi-line string or an optional input file
- [x] **Simulation Loop:**  
- Use the game logic functions (`load_grid_from_string`, `step`, `render_full`, `render_half`) to run the simulation in a loop
- [x] **Display Grid:**  
- Print the grid after each iteration (and optionally pause based on `--delay`)
- [x] **Wiring:**  
- Ensure that the CLI "wires" the game logic together, so that running the script results in a complete simulation cycle
- [x] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #1 increase resolution of life and package it up
 ```

---

### Prompt 8: Wiring the Package Together
- [ ] **Finalize CLI Integration:**  
- In `lifegame/lifegame/cli.py`, ensure the `main()` function properly parses command-line arguments and calls the simulation loop
- [ ] **Update Package Initialization:**  
- Update `lifegame/__init__.py` if necessary to expose key functions
- [ ] **Configure Entry Points:**  
- Modify `pyproject.toml` to add a `console_scripts` entry point so that the CLI can be invoked directly (e.g., via the command "lifegame-run")
- [ ] **Ensure Module Integration:**  
- Ensure that all modules (`game.py` and `cli.py`) are properly imported and that no code is orphaned
- [ ] **Update Documentation:**  
- Add a brief usage section at the top of `lifegame/README.md` explaining how to run the CLI and run tests
- [ ] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #1 increase resolution of life and package it up
 ```

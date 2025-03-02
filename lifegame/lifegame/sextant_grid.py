from typing import NamedTuple, Set, Dict, FrozenSet, Literal, TypeAlias, List, Tuple
from pydantic import BaseModel, Field, validator


# Define a Literal type for valid sextant coordinate strings
SextantCoordinateString: TypeAlias = Literal["1A", "1B", "2A", "2B", "3A", "3B"]

# Define a type for sets of sextant coordinate strings
SextantString: TypeAlias = Set[SextantCoordinateString]

# Constants for coordinate strings
COORD_1A: SextantCoordinateString = "1A"
COORD_1B: SextantCoordinateString = "1B"
COORD_2A: SextantCoordinateString = "2A"
COORD_2B: SextantCoordinateString = "2B"
COORD_3A: SextantCoordinateString = "3A"
COORD_3B: SextantCoordinateString = "3B"


class SextantColumn(NamedTuple):
    column_a: bool
    column_b: bool


class SextantRow(NamedTuple):
    row_1: SextantColumn
    row_2: SextantColumn
    row_3: SextantColumn


class SextantChar(NamedTuple):
    """Represents a sextant Unicode character with its description."""

    unicode: str
    char: str  # Visual representation for source code readability
    description: str = ""

    def __str__(self) -> str:
        """Returns the Unicode character when the object is converted to string."""
        return self.unicode


# Define sextant characters grouped by cell count
class ZeroSextantCellsActivated:
    """Sextant characters with no cells activated."""

    EMPTY = SextantChar("\U0001FB93", "⮓", "Empty sextant")


class OneSextantCellActivated:
    """Sextant characters with one cell activated."""

    TOP_LEFT = SextantChar("\U0001FB00", "🬀", "Top-left cell only")
    TOP_RIGHT = SextantChar("\U0001FB01", "🬁", "Top-right cell only")
    MIDDLE_LEFT = SextantChar("\U0001FB03", "🬃", "Middle-left cell only")
    MIDDLE_RIGHT = SextantChar("\U0001FB07", "🬇", "Middle-right cell only")
    BOTTOM_LEFT = SextantChar("\U0001FB0F", "🬏", "Bottom-left cell only")
    BOTTOM_RIGHT = SextantChar("\U0001FB1E", "🬞", "Bottom-right cell only")


class TwoSextantCellsActivated:
    """Sextant characters with two cells activated."""

    TOP_ROW = SextantChar("\U0001FB02", "🬂", "Top row filled")
    LEFT_TOP_TWO = SextantChar("\U0001FB04", "🬄", "Left column, top two cells")
    TOP_LEFT_MIDDLE_RIGHT = SextantChar("\U0001FB08", "🬈", "Top-left and middle-right")
    LEFT_TOP_BOTTOM = SextantChar("\U0001FB10", "🬐", "Left column, top and bottom")
    TOP_LEFT_BOTTOM_RIGHT = SextantChar("\U0001FB1F", "🬟", "Top-left and bottom-right")
    RIGHT_TOP_TWO = SextantChar("\U0001FB09", "🬉", "Right column, top two cells")
    TOP_RIGHT_BOTTOM_LEFT = SextantChar("\U0001FB11", "🬑", "Top-right and bottom-left")
    RIGHT_TOP_BOTTOM = SextantChar("\U0001FB20", "🬠", "Right column, top and bottom")
    MIDDLE_ROW = SextantChar("\U0001FB0B", "🬋", "Middle row filled")
    LEFT_BOTTOM_TWO = SextantChar("\U0001FB13", "🬓", "Left column, bottom two cells")
    MIDDLE_LEFT_BOTTOM_RIGHT = SextantChar(
        "\U0001FB22", "🬢", "Middle-left and bottom-right"
    )
    MIDDLE_RIGHT_BOTTOM_LEFT = SextantChar(
        "\U0001FB16", "🬖", "Middle-right and bottom-left"
    )
    RIGHT_BOTTOM_TWO = SextantChar("\U0001FB26", "🬦", "Right column, bottom two cells")
    BOTTOM_ROW = SextantChar("\U0001FB2D", "🬭", "Bottom row filled")


class ThreeSextantCellsActivated:
    """Sextant characters with three cells activated."""

    TOP_ROW_MIDDLE_LEFT = SextantChar("\U0001FB06", "🬆", "Top row and middle-left")
    TOP_ROW_MIDDLE_RIGHT = SextantChar("\U0001FB0A", "🬊", "Top row and middle-right")
    TOP_LEFT_MIDDLE_ROW = SextantChar("\U0001FB0C", "🬌", "Top-left and middle row")
    TOP_RIGHT_MIDDLE_ROW = SextantChar("\U0001FB0D", "🬍", "Top-right and middle row")


class FourSextantCellsActivated:
    """Sextant characters with four cells activated."""

    TOP_TWO_ROWS = SextantChar("\U0001FB0E", "🬎", "Top two rows filled")
    TOP_ROW_MIDDLE_RIGHT_BOTTOM_LEFT = SextantChar(
        "\U0001FB19", "🬙", "Top row, middle-right, bottom-left"
    )
    LEFT_COLUMN_MIDDLE_RIGHT_BOTTOM_LEFT = SextantChar(
        "\U0001FB1B", "🬛", "Left column, middle-right, bottom-left"
    )
    TOP_RIGHT_MIDDLE_ROW_BOTTOM_LEFT = SextantChar(
        "\U0001FB1C", "🬜", "Top-right, middle row, bottom-left"
    )
    TOP_ROW_MIDDLE_LEFT_BOTTOM_RIGHT = SextantChar(
        "\U0001FB25", "🬥", "Top row, middle-left, bottom-right"
    )
    TOP_ROW_MIDDLE_RIGHT_BOTTOM_RIGHT = SextantChar(
        "\U0001FB28", "🬨", "Top row, middle-right, bottom-right"
    )
    TOP_LEFT_MIDDLE_ROW_BOTTOM_RIGHT = SextantChar(
        "\U0001FB2A", "🬪", "Top-left, middle row, bottom-right"
    )
    TOP_RIGHT_MIDDLE_ROW_BOTTOM_RIGHT = SextantChar(
        "\U0001FB2B", "🬫", "Top-right, middle row, bottom-right"
    )
    TOP_BOTTOM_ROWS = SextantChar("\U0001FB30", "🬰", "Top and bottom rows filled")
    LEFT_COLUMN_BOTTOM_ROW = SextantChar("\U0001FB32", "🬲", "Left column, bottom row")
    TOP_RIGHT_MIDDLE_LEFT_BOTTOM_ROW = SextantChar(
        "\U0001FB33", "🬳", "Top-right, middle-left, bottom row"
    )
    TOP_LEFT_MIDDLE_RIGHT_BOTTOM_ROW = SextantChar(
        "\U0001FB36", "🬶", "Top-left, middle-right, bottom row"
    )
    TOP_RIGHT_MIDDLE_RIGHT_BOTTOM_ROW = SextantChar(
        "\U0001FB37", "🬷", "Top-right, middle-right, bottom row"
    )
    MIDDLE_BOTTOM_ROWS = SextantChar("\U0001FB39", "🬹", "Middle and bottom rows filled")


class FiveSextantCellsActivated:
    """Sextant characters with five cells activated."""

    ALL_EXCEPT_BOTTOM_RIGHT = SextantChar("\U0001FB1D", "🬝", "All except bottom-right")
    ALL_EXCEPT_BOTTOM_LEFT = SextantChar("\U0001FB2C", "🬬", "All except bottom-left")
    ALL_EXCEPT_MIDDLE_RIGHT = SextantChar("\U0001FB34", "🬴", "All except middle-right")
    ALL_EXCEPT_MIDDLE_LEFT = SextantChar("\U0001FB38", "🬸", "All except middle-left")
    ALL_EXCEPT_TOP_RIGHT = SextantChar("\U0001FB3A", "🬺", "All except top-right")
    ALL_EXCEPT_TOP_LEFT = SextantChar("\U0001FB3B", "🬻", "All except top-left")


class SixSextantCellsActivated:
    """Sextant characters with all six cells activated."""

    FULL_BLOCK = SextantChar("\U0001FB8B", "🮋", "All cells filled (full block)")


class SextantCoordinate(BaseModel):
    row: int = Field(..., ge=1, le=3)
    col: Literal["A", "B"]

    @validator("col")
    def validate_col(cls, v):
        if v not in {"A", "B"}:
            raise ValueError('Column must be "A" or "B"')
        return v

    @classmethod
    def from_string(cls, coord_str: SextantCoordinateString):
        if len(coord_str) != 2:
            raise ValueError("Coordinate string must be of length 2")
        row_part, col_part = coord_str
        try:
            row = int(row_part)
        except ValueError:
            raise ValueError("Row must be an integer between 1 and 3")
        return cls(row=row, col=col_part.upper())


class SextantCoordMapping(NamedTuple):
    """Mapping between a set of coordinates and a Unicode character."""

    coordinate_strings: Tuple[SextantCoordinateString, ...]
    sextant_char: SextantChar

    @property
    def unicode_char(self) -> str:
        """Returns the Unicode character for backward compatibility."""
        return self.sextant_char.unicode


# Function to convert mappings to a dictionary with frozensets as keys
def create_sextant_dict(
    mappings: List[SextantCoordMapping],
) -> Dict[FrozenSet[SextantCoordinateString], str]:
    return {frozenset(m.coordinate_strings): m.sextant_char.unicode for m in mappings}


# Define all the sextant mappings organized by cell count
SEXTANT_MAPPINGS_BY_COUNT: List[List[SextantCoordMapping]] = [
    # 0 cells
    [
        SextantCoordMapping((), ZeroSextantCellsActivated.EMPTY),
    ],
    # 1 cell
    [
        SextantCoordMapping((COORD_1A,), OneSextantCellActivated.TOP_LEFT),
        SextantCoordMapping((COORD_1B,), OneSextantCellActivated.TOP_RIGHT),
        SextantCoordMapping((COORD_2A,), OneSextantCellActivated.MIDDLE_LEFT),
        SextantCoordMapping((COORD_2B,), OneSextantCellActivated.MIDDLE_RIGHT),
        SextantCoordMapping((COORD_3A,), OneSextantCellActivated.BOTTOM_LEFT),
        SextantCoordMapping((COORD_3B,), OneSextantCellActivated.BOTTOM_RIGHT),
    ],
    # 2 cells
    [
        SextantCoordMapping((COORD_1A, COORD_1B), TwoSextantCellsActivated.TOP_ROW),
        SextantCoordMapping(
            (COORD_1A, COORD_2A), TwoSextantCellsActivated.LEFT_TOP_TWO
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2B), TwoSextantCellsActivated.TOP_LEFT_MIDDLE_RIGHT
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_3A), TwoSextantCellsActivated.LEFT_TOP_BOTTOM
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_3B), TwoSextantCellsActivated.TOP_LEFT_BOTTOM_RIGHT
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2B), TwoSextantCellsActivated.RIGHT_TOP_TWO
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_3A), TwoSextantCellsActivated.TOP_RIGHT_BOTTOM_LEFT
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_3B), TwoSextantCellsActivated.RIGHT_TOP_BOTTOM
        ),
        SextantCoordMapping((COORD_2A, COORD_2B), TwoSextantCellsActivated.MIDDLE_ROW),
        SextantCoordMapping(
            (COORD_2A, COORD_3A), TwoSextantCellsActivated.LEFT_BOTTOM_TWO
        ),
        SextantCoordMapping(
            (COORD_2A, COORD_3B), TwoSextantCellsActivated.MIDDLE_LEFT_BOTTOM_RIGHT
        ),
        SextantCoordMapping(
            (COORD_2B, COORD_3A), TwoSextantCellsActivated.MIDDLE_RIGHT_BOTTOM_LEFT
        ),
        SextantCoordMapping(
            (COORD_2B, COORD_3B), TwoSextantCellsActivated.RIGHT_BOTTOM_TWO
        ),
        SextantCoordMapping((COORD_3A, COORD_3B), TwoSextantCellsActivated.BOTTOM_ROW),
    ],
    # 3 cells
    [
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A),
            ThreeSextantCellsActivated.TOP_ROW_MIDDLE_LEFT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2B),
            ThreeSextantCellsActivated.TOP_ROW_MIDDLE_RIGHT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_2B),
            ThreeSextantCellsActivated.TOP_LEFT_MIDDLE_ROW,
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_2B),
            ThreeSextantCellsActivated.TOP_RIGHT_MIDDLE_ROW,
        ),
    ],
    # 4 cells
    [
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_2B),
            FourSextantCellsActivated.TOP_TWO_ROWS,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2B, COORD_3A),
            FourSextantCellsActivated.TOP_ROW_MIDDLE_RIGHT_BOTTOM_LEFT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_2B, COORD_3A),
            FourSextantCellsActivated.LEFT_COLUMN_MIDDLE_RIGHT_BOTTOM_LEFT,
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_2B, COORD_3A),
            FourSextantCellsActivated.TOP_RIGHT_MIDDLE_ROW_BOTTOM_LEFT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_3B),
            FourSextantCellsActivated.TOP_ROW_MIDDLE_LEFT_BOTTOM_RIGHT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2B, COORD_3B),
            FourSextantCellsActivated.TOP_ROW_MIDDLE_RIGHT_BOTTOM_RIGHT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_2B, COORD_3B),
            FourSextantCellsActivated.TOP_LEFT_MIDDLE_ROW_BOTTOM_RIGHT,
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_2B, COORD_3B),
            FourSextantCellsActivated.TOP_RIGHT_MIDDLE_ROW_BOTTOM_RIGHT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_3A, COORD_3B),
            FourSextantCellsActivated.TOP_BOTTOM_ROWS,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_3A, COORD_3B),
            FourSextantCellsActivated.LEFT_COLUMN_BOTTOM_ROW,
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_3A, COORD_3B),
            FourSextantCellsActivated.TOP_RIGHT_MIDDLE_LEFT_BOTTOM_ROW,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2B, COORD_3A, COORD_3B),
            FourSextantCellsActivated.TOP_LEFT_MIDDLE_RIGHT_BOTTOM_ROW,
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2B, COORD_3A, COORD_3B),
            FourSextantCellsActivated.TOP_RIGHT_MIDDLE_RIGHT_BOTTOM_ROW,
        ),
        SextantCoordMapping(
            (COORD_2A, COORD_2B, COORD_3A, COORD_3B),
            FourSextantCellsActivated.MIDDLE_BOTTOM_ROWS,
        ),
    ],
    # 5 cells
    [
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_2B, COORD_3A),
            FiveSextantCellsActivated.ALL_EXCEPT_BOTTOM_RIGHT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_2B, COORD_3B),
            FiveSextantCellsActivated.ALL_EXCEPT_BOTTOM_LEFT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_3A, COORD_3B),
            FiveSextantCellsActivated.ALL_EXCEPT_MIDDLE_RIGHT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2B, COORD_2B, COORD_3A, COORD_3B),
            FiveSextantCellsActivated.ALL_EXCEPT_MIDDLE_LEFT,
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_2B, COORD_3A, COORD_3B),
            FiveSextantCellsActivated.ALL_EXCEPT_TOP_RIGHT,
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_2B, COORD_3A, COORD_3B),
            FiveSextantCellsActivated.ALL_EXCEPT_TOP_LEFT,
        ),
    ],
    # 6 cells
    [
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_2B, COORD_3A, COORD_3B),
            SixSextantCellsActivated.FULL_BLOCK,
        ),
    ],
]

# Flatten the list for operations that need all mappings
ALL_SEXTANT_MAPPINGS = [
    mapping for sublist in SEXTANT_MAPPINGS_BY_COUNT for mapping in sublist
]

# Create dictionaries for each cell count
CELL_MAPPINGS_BY_ACTIVE_CELLS = tuple(
    create_sextant_dict(mappings) for mappings in SEXTANT_MAPPINGS_BY_COUNT
)

# Create the main mapping dictionary
SEXTANT_CHAR_MAP = create_sextant_dict(ALL_SEXTANT_MAPPINGS)

# Create a mapping from sets of SextantCoordinate objects to Unicode characters
SEXTANT_MAP: Dict[FrozenSet[SextantCoordinate], str] = {
    frozenset(SextantCoordinate.from_string(coord) for coord in coords): char
    for coords, char in SEXTANT_CHAR_MAP.items()
}


def get_sextant_character(active_cells: Set[SextantCoordinate]) -> str:
    """Returns the correct Unicode sextant character based on active cells."""
    return SEXTANT_MAP.get(frozenset(active_cells), "?")  # Return '?' if not found

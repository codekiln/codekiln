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
    unicode_char: str
    description: str = ""  # Optional description of the pattern


# Function to convert mappings to a dictionary with frozensets as keys
def create_sextant_dict(
    mappings: List[SextantCoordMapping],
) -> Dict[FrozenSet[SextantCoordinateString], str]:
    return {frozenset(m.coordinate_strings): m.unicode_char for m in mappings}


# Define all the sextant mappings organized by cell count
SEXTANT_MAPPINGS_BY_COUNT: List[List[SextantCoordMapping]] = [
    # 0 cells
    [
        SextantCoordMapping((), "\U0001FB93", "Empty sextant"),
    ],
    # 1 cell
    [
        SextantCoordMapping((COORD_1A,), "\U0001FB00", "Top-left cell only"),
        SextantCoordMapping((COORD_1B,), "\U0001FB01", "Top-right cell only"),
        SextantCoordMapping((COORD_2A,), "\U0001FB03", "Middle-left cell only"),
        SextantCoordMapping((COORD_2B,), "\U0001FB07", "Middle-right cell only"),
        SextantCoordMapping((COORD_3A,), "\U0001FB0F", "Bottom-left cell only"),
        SextantCoordMapping((COORD_3B,), "\U0001FB1E", "Bottom-right cell only"),
    ],
    # 2 cells
    [
        SextantCoordMapping((COORD_1A, COORD_1B), "\U0001FB02", "Top row filled"),
        SextantCoordMapping(
            (COORD_1A, COORD_2A), "\U0001FB04", "Left column, top two cells"
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2B), "\U0001FB08", "Top-left and middle-right"
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_3A), "\U0001FB10", "Left column, top and bottom"
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_3B), "\U0001FB1F", "Top-left and bottom-right"
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2B), "\U0001FB09", "Right column, top two cells"
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_3A), "\U0001FB11", "Top-right and bottom-left"
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_3B), "\U0001FB20", "Right column, top and bottom"
        ),
        SextantCoordMapping((COORD_2A, COORD_2B), "\U0001FB0B", "Middle row filled"),
        SextantCoordMapping(
            (COORD_2A, COORD_3A), "\U0001FB13", "Left column, bottom two cells"
        ),
        SextantCoordMapping(
            (COORD_2A, COORD_3B), "\U0001FB22", "Middle-left and bottom-right"
        ),
        SextantCoordMapping(
            (COORD_2B, COORD_3A), "\U0001FB16", "Middle-right and bottom-left"
        ),
        SextantCoordMapping(
            (COORD_2B, COORD_3B), "\U0001FB26", "Right column, bottom two cells"
        ),
        SextantCoordMapping((COORD_3A, COORD_3B), "\U0001FB2D", "Bottom row filled"),
    ],
    # 3 cells
    [
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A), "\U0001FB06", "Top row and middle-left"
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2B), "\U0001FB0A", "Top row and middle-right"
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_2B), "\U0001FB0C", "Top-left and middle row"
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_2B), "\U0001FB0D", "Top-right and middle row"
        ),
    ],
    # 4 cells
    [
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_2B),
            "\U0001FB0E",
            "Top two rows filled",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2B, COORD_3A),
            "\U0001FB19",
            "Top row, middle-right, bottom-left",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_2B, COORD_3A),
            "\U0001FB1B",
            "Left column, middle-right, bottom-left",
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_2B, COORD_3A),
            "\U0001FB1C",
            "Top-right, middle row, bottom-left",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_3B),
            "\U0001FB25",
            "Top row, middle-left, bottom-right",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2B, COORD_3B),
            "\U0001FB28",
            "Top row, middle-right, bottom-right",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_2B, COORD_3B),
            "\U0001FB2A",
            "Top-left, middle row, bottom-right",
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_2B, COORD_3B),
            "\U0001FB2B",
            "Top-right, middle row, bottom-right",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_3A, COORD_3B),
            "\U0001FB30",
            "Top and bottom rows filled",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_3A, COORD_3B),
            "\U0001FB32",
            "Left column, bottom row",
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_3A, COORD_3B),
            "\U0001FB33",
            "Top-right, middle-left, bottom row",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2B, COORD_3A, COORD_3B),
            "\U0001FB36",
            "Top-left, middle-right, bottom row",
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2B, COORD_3A, COORD_3B),
            "\U0001FB37",
            "Top-right, middle-right, bottom row",
        ),
        SextantCoordMapping(
            (COORD_2A, COORD_2B, COORD_3A, COORD_3B),
            "\U0001FB39",
            "Middle and bottom rows filled",
        ),
    ],
    # 5 cells
    [
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_2B, COORD_3A),
            "\U0001FB1D",
            "All except bottom-right",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_2B, COORD_3B),
            "\U0001FB2C",
            "All except bottom-left",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_3A, COORD_3B),
            "\U0001FB34",
            "All except middle-right",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2B, COORD_2B, COORD_3A, COORD_3B),
            "\U0001FB38",
            "All except middle-left",
        ),
        SextantCoordMapping(
            (COORD_1A, COORD_2A, COORD_2B, COORD_3A, COORD_3B),
            "\U0001FB3A",
            "All except top-right",
        ),
        SextantCoordMapping(
            (COORD_1B, COORD_2A, COORD_2B, COORD_3A, COORD_3B),
            "\U0001FB3B",
            "All except top-left",
        ),
    ],
    # 6 cells
    [
        SextantCoordMapping(
            (COORD_1A, COORD_1B, COORD_2A, COORD_2B, COORD_3A, COORD_3B),
            "\U0001FB8B",
            "All cells filled (full block)",
        ),
    ],
]

# Flatten the list for operations that need all mappings
ALL_SEXTANT_MAPPINGS = [
    mapping for sublist in SEXTANT_MAPPINGS_BY_COUNT for mapping in sublist
]

# Create dictionaries for each cell count
CELLS_BY_COUNT = tuple(
    create_sextant_dict(mappings) for mappings in SEXTANT_MAPPINGS_BY_COUNT
)

# For backward compatibility and readability, create named constants
ZERO_CELLS = CELLS_BY_COUNT[0]
ONE_CELL = CELLS_BY_COUNT[1]
TWO_CELLS = CELLS_BY_COUNT[2]
THREE_CELLS = CELLS_BY_COUNT[3]
FOUR_CELLS = CELLS_BY_COUNT[4]
FIVE_CELLS = CELLS_BY_COUNT[5]
SIX_CELLS = CELLS_BY_COUNT[6]

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

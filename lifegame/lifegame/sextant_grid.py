from typing import (
    NamedTuple,
    Set,
    Dict,
    FrozenSet,
    Literal,
    TypeAlias,
    List,
    Tuple,
    ClassVar,
    Type,
    AbstractType,
)
from pydantic import BaseModel, Field, validator
from abc import ABC, abstractmethod


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


class SextantCoordMapping(NamedTuple):
    """Mapping between a set of coordinates and a Unicode character."""

    coordinate_strings: Tuple[SextantCoordinateString, ...]
    sextant_char: SextantChar

    @property
    def unicode_char(self) -> str:
        """Returns the Unicode character for backward compatibility."""
        return self.sextant_char.unicode


class SextantCellsActivated(ABC):
    """Abstract base class for sextant character groups by cell count."""

    @classmethod
    @abstractmethod
    def get_coordinate_mappings(cls) -> List[SextantCoordMapping]:
        """Returns a list of coordinate mappings for this cell count."""
        pass

    @classmethod
    def cell_count(cls) -> int:
        """Returns the number of cells activated for this class."""
        # Extract the number from the class name
        for part in cls.__name__.split("Sextant"):
            if part.endswith("CellsActivated"):
                num_str = part.split("Cells")[0]
                if num_str == "Zero":
                    return 0
                elif num_str == "One":
                    return 1
                elif num_str == "Two":
                    return 2
                elif num_str == "Three":
                    return 3
                elif num_str == "Four":
                    return 4
                elif num_str == "Five":
                    return 5
                elif num_str == "Six":
                    return 6
        return -1  # Should never happen

    @staticmethod
    def _create_coord_mapping(
        coords_to_chars: Dict[Tuple[SextantCoordinateString, ...], SextantChar]
    ) -> List[SextantCoordMapping]:
        """Helper method to create coordinate mappings from a dictionary of coordinates to characters.

        Args:
            coords_to_chars: Dictionary mapping coordinate tuples to sextant characters

        Returns:
            List of SextantCoordMapping objects
        """
        return [
            SextantCoordMapping(coords, char)
            for coords, char in coords_to_chars.items()
        ]


# Define sextant characters grouped by cell count
class ZeroSextantCellsActivated(SextantCellsActivated):
    """Sextant characters with no cells activated."""

    EMPTY = SextantChar("\U0001FB93", "⮓", "Empty sextant")

    @classmethod
    def get_coordinate_mappings(cls) -> List[SextantCoordMapping]:
        return cls._create_coord_mapping(
            {
                (): cls.EMPTY,
            }
        )


class OneSextantCellActivated(SextantCellsActivated):
    """Sextant characters with one cell activated."""

    TOP_LEFT = SextantChar("\U0001FB00", "🬀", "Top-left cell only")
    TOP_RIGHT = SextantChar("\U0001FB01", "🬁", "Top-right cell only")
    MIDDLE_LEFT = SextantChar("\U0001FB03", "🬃", "Middle-left cell only")
    MIDDLE_RIGHT = SextantChar("\U0001FB07", "🬇", "Middle-right cell only")
    BOTTOM_LEFT = SextantChar("\U0001FB0F", "🬏", "Bottom-left cell only")
    BOTTOM_RIGHT = SextantChar("\U0001FB1E", "🬞", "Bottom-right cell only")

    @classmethod
    def get_coordinate_mappings(cls) -> List[SextantCoordMapping]:
        return cls._create_coord_mapping(
            {
                (COORD_1A,): cls.TOP_LEFT,
                (COORD_1B,): cls.TOP_RIGHT,
                (COORD_2A,): cls.MIDDLE_LEFT,
                (COORD_2B,): cls.MIDDLE_RIGHT,
                (COORD_3A,): cls.BOTTOM_LEFT,
                (COORD_3B,): cls.BOTTOM_RIGHT,
            }
        )


class TwoSextantCellsActivated(SextantCellsActivated):
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

    @classmethod
    def get_coordinate_mappings(cls) -> List[SextantCoordMapping]:
        return cls._create_coord_mapping(
            {
                (COORD_1A, COORD_1B): cls.TOP_ROW,
                (COORD_1A, COORD_2A): cls.LEFT_TOP_TWO,
                (COORD_1A, COORD_2B): cls.TOP_LEFT_MIDDLE_RIGHT,
                (COORD_1A, COORD_3A): cls.LEFT_TOP_BOTTOM,
                (COORD_1A, COORD_3B): cls.TOP_LEFT_BOTTOM_RIGHT,
                (COORD_1B, COORD_2B): cls.RIGHT_TOP_TWO,
                (COORD_1B, COORD_3A): cls.TOP_RIGHT_BOTTOM_LEFT,
                (COORD_1B, COORD_3B): cls.RIGHT_TOP_BOTTOM,
                (COORD_2A, COORD_2B): cls.MIDDLE_ROW,
                (COORD_2A, COORD_3A): cls.LEFT_BOTTOM_TWO,
                (COORD_2A, COORD_3B): cls.MIDDLE_LEFT_BOTTOM_RIGHT,
                (COORD_2B, COORD_3A): cls.MIDDLE_RIGHT_BOTTOM_LEFT,
                (COORD_2B, COORD_3B): cls.RIGHT_BOTTOM_TWO,
                (COORD_3A, COORD_3B): cls.BOTTOM_ROW,
            }
        )


class ThreeSextantCellsActivated(SextantCellsActivated):
    """Sextant characters with three cells activated."""

    TOP_ROW_MIDDLE_LEFT = SextantChar("\U0001FB06", "🬆", "Top row and middle-left")
    TOP_ROW_MIDDLE_RIGHT = SextantChar("\U0001FB0A", "🬊", "Top row and middle-right")
    TOP_LEFT_MIDDLE_ROW = SextantChar("\U0001FB0C", "🬌", "Top-left and middle row")
    TOP_RIGHT_MIDDLE_ROW = SextantChar("\U0001FB0D", "🬍", "Top-right and middle row")

    @classmethod
    def get_coordinate_mappings(cls) -> List[SextantCoordMapping]:
        return cls._create_coord_mapping(
            {
                (COORD_1A, COORD_1B, COORD_2A): cls.TOP_ROW_MIDDLE_LEFT,
                (COORD_1A, COORD_1B, COORD_2B): cls.TOP_ROW_MIDDLE_RIGHT,
                (COORD_1A, COORD_2A, COORD_2B): cls.TOP_LEFT_MIDDLE_ROW,
                (COORD_1B, COORD_2A, COORD_2B): cls.TOP_RIGHT_MIDDLE_ROW,
            }
        )


class FourSextantCellsActivated(SextantCellsActivated):
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

    @classmethod
    def get_coordinate_mappings(cls) -> List[SextantCoordMapping]:
        return cls._create_coord_mapping(
            {
                (COORD_1A, COORD_1B, COORD_2A, COORD_2B): cls.TOP_TWO_ROWS,
                (
                    COORD_1A,
                    COORD_1B,
                    COORD_2B,
                    COORD_3A,
                ): cls.TOP_ROW_MIDDLE_RIGHT_BOTTOM_LEFT,
                (
                    COORD_1A,
                    COORD_2A,
                    COORD_2B,
                    COORD_3A,
                ): cls.LEFT_COLUMN_MIDDLE_RIGHT_BOTTOM_LEFT,
                (
                    COORD_1B,
                    COORD_2A,
                    COORD_2B,
                    COORD_3A,
                ): cls.TOP_RIGHT_MIDDLE_ROW_BOTTOM_LEFT,
                (
                    COORD_1A,
                    COORD_1B,
                    COORD_2A,
                    COORD_3B,
                ): cls.TOP_ROW_MIDDLE_LEFT_BOTTOM_RIGHT,
                (
                    COORD_1A,
                    COORD_1B,
                    COORD_2B,
                    COORD_3B,
                ): cls.TOP_ROW_MIDDLE_RIGHT_BOTTOM_RIGHT,
                (
                    COORD_1A,
                    COORD_2A,
                    COORD_2B,
                    COORD_3B,
                ): cls.TOP_LEFT_MIDDLE_ROW_BOTTOM_RIGHT,
                (
                    COORD_1B,
                    COORD_2A,
                    COORD_2B,
                    COORD_3B,
                ): cls.TOP_RIGHT_MIDDLE_ROW_BOTTOM_RIGHT,
                (COORD_1A, COORD_1B, COORD_3A, COORD_3B): cls.TOP_BOTTOM_ROWS,
                (COORD_1A, COORD_2A, COORD_3A, COORD_3B): cls.LEFT_COLUMN_BOTTOM_ROW,
                (
                    COORD_1B,
                    COORD_2A,
                    COORD_3A,
                    COORD_3B,
                ): cls.TOP_RIGHT_MIDDLE_LEFT_BOTTOM_ROW,
                (
                    COORD_1A,
                    COORD_2B,
                    COORD_3A,
                    COORD_3B,
                ): cls.TOP_LEFT_MIDDLE_RIGHT_BOTTOM_ROW,
                (
                    COORD_1B,
                    COORD_2B,
                    COORD_3A,
                    COORD_3B,
                ): cls.TOP_RIGHT_MIDDLE_RIGHT_BOTTOM_ROW,
                (COORD_2A, COORD_2B, COORD_3A, COORD_3B): cls.MIDDLE_BOTTOM_ROWS,
            }
        )


class FiveSextantCellsActivated(SextantCellsActivated):
    """Sextant characters with five cells activated."""

    ALL_EXCEPT_BOTTOM_RIGHT = SextantChar("\U0001FB1D", "🬝", "All except bottom-right")
    ALL_EXCEPT_BOTTOM_LEFT = SextantChar("\U0001FB2C", "🬬", "All except bottom-left")
    ALL_EXCEPT_MIDDLE_RIGHT = SextantChar("\U0001FB34", "🬴", "All except middle-right")
    ALL_EXCEPT_MIDDLE_LEFT = SextantChar("\U0001FB38", "🬸", "All except middle-left")
    ALL_EXCEPT_TOP_RIGHT = SextantChar("\U0001FB3A", "🬺", "All except top-right")
    ALL_EXCEPT_TOP_LEFT = SextantChar("\U0001FB3B", "🬻", "All except top-left")

    @classmethod
    def get_coordinate_mappings(cls) -> List[SextantCoordMapping]:
        return cls._create_coord_mapping(
            {
                (
                    COORD_1A,
                    COORD_1B,
                    COORD_2A,
                    COORD_2B,
                    COORD_3A,
                ): cls.ALL_EXCEPT_BOTTOM_RIGHT,
                (
                    COORD_1A,
                    COORD_1B,
                    COORD_2A,
                    COORD_2B,
                    COORD_3B,
                ): cls.ALL_EXCEPT_BOTTOM_LEFT,
                (
                    COORD_1A,
                    COORD_1B,
                    COORD_2A,
                    COORD_3A,
                    COORD_3B,
                ): cls.ALL_EXCEPT_MIDDLE_RIGHT,
                (
                    COORD_1A,
                    COORD_2B,
                    COORD_2B,
                    COORD_3A,
                    COORD_3B,
                ): cls.ALL_EXCEPT_MIDDLE_LEFT,
                (
                    COORD_1A,
                    COORD_2A,
                    COORD_2B,
                    COORD_3A,
                    COORD_3B,
                ): cls.ALL_EXCEPT_TOP_RIGHT,
                (
                    COORD_1B,
                    COORD_2A,
                    COORD_2B,
                    COORD_3A,
                    COORD_3B,
                ): cls.ALL_EXCEPT_TOP_LEFT,
            }
        )


class SixSextantCellsActivated(SextantCellsActivated):
    """Sextant characters with all six cells activated."""

    FULL_BLOCK = SextantChar("\U0001FB8B", "🮋", "All cells filled (full block)")

    @classmethod
    def get_coordinate_mappings(cls) -> List[SextantCoordMapping]:
        return cls._create_coord_mapping(
            {
                (
                    COORD_1A,
                    COORD_1B,
                    COORD_2A,
                    COORD_2B,
                    COORD_3A,
                    COORD_3B,
                ): cls.FULL_BLOCK,
            }
        )


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


# Function to convert mappings to a dictionary with frozensets as keys
def create_sextant_dict(
    mappings: List[SextantCoordMapping],
) -> Dict[FrozenSet[SextantCoordinateString], str]:
    return {frozenset(m.coordinate_strings): m.sextant_char.unicode for m in mappings}


# List of sextant cell classes in order of cell count
SEXTANT_CELL_CLASSES: List[Type[SextantCellsActivated]] = [
    ZeroSextantCellsActivated,
    OneSextantCellActivated,
    TwoSextantCellsActivated,
    ThreeSextantCellsActivated,
    FourSextantCellsActivated,
    FiveSextantCellsActivated,
    SixSextantCellsActivated,
]

# Get mappings from each class
SEXTANT_MAPPINGS_BY_COUNT: List[List[SextantCoordMapping]] = [
    cls.get_coordinate_mappings() for cls in SEXTANT_CELL_CLASSES
]

# Create dictionaries for each cell count
CELL_MAPPINGS_BY_ACTIVE_CELLS = tuple(
    create_sextant_dict(mappings) for mappings in SEXTANT_MAPPINGS_BY_COUNT
)

# Create the main mapping dictionary from the flattened cell mappings
SEXTANT_CHAR_MAP = {
    coords: char
    for cell_count_dict in CELL_MAPPINGS_BY_ACTIVE_CELLS
    for coords, char in cell_count_dict.items()
}

# Create a mapping from sets of SextantCoordinate objects to Unicode characters
SEXTANT_MAP: Dict[FrozenSet[SextantCoordinate], str] = {
    frozenset(SextantCoordinate.from_string(coord) for coord in coords): char
    for coords, char in SEXTANT_CHAR_MAP.items()
}


def get_sextant_character(active_cells: Set[SextantCoordinate]) -> str:
    """Returns the correct Unicode sextant character based on active cells."""
    return SEXTANT_MAP.get(frozenset(active_cells), "?")  # Return '?' if not found

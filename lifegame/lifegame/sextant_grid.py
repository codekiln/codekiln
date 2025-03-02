from typing import NamedTuple, Set, List, Dict, FrozenSet
from pydantic import BaseModel, Field, validator
from typing import Literal


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
    def from_string(cls, coord_str: str):
        if len(coord_str) != 2:
            raise ValueError("Coordinate string must be of length 2")
        row_part, col_part = coord_str
        try:
            row = int(row_part)
        except ValueError:
            raise ValueError("Row must be an integer between 1 and 3")
        return cls(row=row, col=col_part.upper())


ZERO_CELLS: Dict[List[str], str] = {
    (): "🮓",  # U+1FB93
}

ONE_CELL: Dict[List[str], str] = {
    ["1A"]: "🬀",  # U+1FB00
    ["1B"]: "🬁",  # U+1FB01
    ["2A"]: "🬃",  # U+1FB03
    ["2B"]: "🬇",  # U+1FB07
    ["3A"]: "🬏",  # U+1FB0F
    ["3B"]: "🬞",  # U+1FB1E
}

TWO_CELLS: Dict[List[str], str] = {
    ["1A", "1B"]: "🬂",  # U+1FB02
    ["1A", "2A"]: "🬄",  # U+1FB04
    ["1A", "2B"]: "🬈",  # U+1FB08
    ["1A", "3A"]: "🬐",  # U+1FB10
    ["1A", "3B"]: "🬟",  # U+1FB1F
    ["1B", "2B"]: "🬉",  # U+1FB09
    ["1B", "3A"]: "🬑",  # U+1FB11
    ["1B", "3B"]: "🬠",  # U+1FB20
    ["2A", "2B"]: "🬋",  # U+1FB0B
    ["2A", "3A"]: "🬓",  # U+1FB13
    ["2A", "3B"]: "🬢",  # U+1FB22
    ["2B", "3A"]: "🬖",  # U+1FB16
    ["2B", "3B"]: "🬦",  # U+1FB26
    ["3A", "3B"]: "🬭",  # U+1FB2D
}

THREE_CELLS: Dict[List[str], str] = {
    ["1A", "1B", "2A"]: "🬆",
    ["1A", "1B", "2B"]: "🬊",
    ["1A", "2A", "2B"]: "🬌",
    ["1B", "2A", "2B"]: "🬍",
}

FOUR_CELLS: Dict[List[str], str] = {
    ["1A", "1B", "2A", "2B"]: "🬎",
    ["1A", "2A", "1B", "2B"]: "🬕",
    ["1A", "1B", "2B", "3A"]: "🬙",
    ["1A", "2A", "2B", "3A"]: "🬛",
    ["1B", "2A", "2B", "3A"]: "🬜",
    ["1A", "1B", "2A", "3B"]: "🬥",
    ["1A", "1B", "2B", "3B"]: "🬨",
    ["1A", "2A", "2B", "3B"]: "🬪",
    ["1B", "2A", "2B", "3B"]: "🬫",
    ["1A", "1B", "3A", "3B"]: "🬰",
    ["1A", "2A", "3A", "3B"]: "🬲",
    ["1B", "2A", "3A", "3B"]: "🬳",
    ["1A", "2B", "3A", "3B"]: "🬶",
    ["1B", "2B", "3A", "3B"]: "🬷",
    ["2A", "2B", "3A", "3B"]: "🬹",
}

FIVE_CELLS: Dict[List[str], str] = {
    ["1A", "1B", "2A", "2B", "3A"]: "🬝",
    ["1A", "1B", "2A", "2B", "3B"]: "🬬",
    ["1A", "1B", "2A", "3A", "3B"]: "🬴",
    ["1A", "2B", "2B", "3A", "3B"]: "🬸",
    ["1A", "2A", "2B", "3A", "3B"]: "🬺",
    ["1B", "2A", "2B", "3A", "3B"]: "🬻",
}

SIX_CELLS: Dict[List[str], str] = {
    ["1A", "1B", "2A", "2B", "3A", "3B"]: "🮋",
}


SEXTANT_MAP: Dict[FrozenSet[SextantCoordinate], str] = {
    frozenset(SextantCoordinate.from_string(coord) for coord in coords): char
    for cell_map in [
        ZERO_CELLS,
        ONE_CELL,
        TWO_CELLS,
        THREE_CELLS,
        FOUR_CELLS,
        FIVE_CELLS,
        SIX_CELLS,
    ]
    for coords, char in cell_map.items()
}


def get_sextant_character(active_cells: Set[SextantCoordinate]) -> str:
    """Returns the correct Unicode sextant character based on active cells."""
    return SEXTANT_MAP.get(frozenset(active_cells), "?")  # Return '?' if not found

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
    (): "\U0001FB93",  # 🮓 - Empty sextant
}

ONE_CELL: Dict[List[str], str] = {
    ["1A"]: "\U0001FB00",  # 🬀 - Top-left cell only
    ["1B"]: "\U0001FB01",  # 🬁 - Top-right cell only
    ["2A"]: "\U0001FB03",  # 🬃 - Middle-left cell only
    ["2B"]: "\U0001FB07",  # 🬇 - Middle-right cell only
    ["3A"]: "\U0001FB0F",  # 🬏 - Bottom-left cell only
    ["3B"]: "\U0001FB1E",  # 🬞 - Bottom-right cell only
}

TWO_CELLS: Dict[List[str], str] = {
    ["1A", "1B"]: "\U0001FB02",  # 🬂 - Top row filled
    ["1A", "2A"]: "\U0001FB04",  # 🬄 - Left column, top two cells
    ["1A", "2B"]: "\U0001FB08",  # 🬈 - Top-left and middle-right
    ["1A", "3A"]: "\U0001FB10",  # 🬐 - Left column, top and bottom
    ["1A", "3B"]: "\U0001FB1F",  # 🬟 - Top-left and bottom-right
    ["1B", "2B"]: "\U0001FB09",  # 🬉 - Right column, top two cells
    ["1B", "3A"]: "\U0001FB11",  # 🬑 - Top-right and bottom-left
    ["1B", "3B"]: "\U0001FB20",  # 🬠 - Right column, top and bottom
    ["2A", "2B"]: "\U0001FB0B",  # 🬋 - Middle row filled
    ["2A", "3A"]: "\U0001FB13",  # 🬓 - Left column, bottom two cells
    ["2A", "3B"]: "\U0001FB22",  # 🬢 - Middle-left and bottom-right
    ["2B", "3A"]: "\U0001FB16",  # 🬖 - Middle-right and bottom-left
    ["2B", "3B"]: "\U0001FB26",  # 🬦 - Right column, bottom two cells
    ["3A", "3B"]: "\U0001FB2D",  # 🬭 - Bottom row filled
}

THREE_CELLS: Dict[List[str], str] = {
    ["1A", "1B", "2A"]: "\U0001FB06",  # 🬆 - Top row and middle-left
    ["1A", "1B", "2B"]: "\U0001FB0A",  # 🬊 - Top row and middle-right
    ["1A", "2A", "2B"]: "\U0001FB0C",  # 🬌 - Top-left and middle row
    ["1B", "2A", "2B"]: "\U0001FB0D",  # 🬍 - Top-right and middle row
}

FOUR_CELLS: Dict[List[str], str] = {
    ["1A", "1B", "2A", "2B"]: "\U0001FB0E",  # 🬎 - Top two rows filled
    ["1A", "2A", "1B", "2B"]: "\U0001FB15",  # 🬕 - 2x2 grid pattern
    ["1A", "1B", "2B", "3A"]: "\U0001FB19",  # 🬙 - Top row, middle-right, bottom-left
    [
        "1A",
        "2A",
        "2B",
        "3A",
    ]: "\U0001FB1B",  # 🬛 - Left column, middle-right, bottom-left
    ["1B", "2A", "2B", "3A"]: "\U0001FB1C",  # 🬜 - Top-right, middle row, bottom-left
    ["1A", "1B", "2A", "3B"]: "\U0001FB25",  # 🬥 - Top row, middle-left, bottom-right
    ["1A", "1B", "2B", "3B"]: "\U0001FB28",  # 🬨 - Top row, middle-right, bottom-right
    ["1A", "2A", "2B", "3B"]: "\U0001FB2A",  # 🬪 - Top-left, middle row, bottom-right
    ["1B", "2A", "2B", "3B"]: "\U0001FB2B",  # 🬫 - Top-right, middle row, bottom-right
    ["1A", "1B", "3A", "3B"]: "\U0001FB30",  # 🬰 - Top and bottom rows filled
    ["1A", "2A", "3A", "3B"]: "\U0001FB32",  # 🬲 - Left column, bottom row
    ["1B", "2A", "3A", "3B"]: "\U0001FB33",  # 🬳 - Top-right, middle-left, bottom row
    ["1A", "2B", "3A", "3B"]: "\U0001FB36",  # 🬶 - Top-left, middle-right, bottom row
    ["1B", "2B", "3A", "3B"]: "\U0001FB37",  # 🬷 - Top-right, middle-right, bottom row
    ["2A", "2B", "3A", "3B"]: "\U0001FB39",  # 🬹 - Middle and bottom rows filled
}

FIVE_CELLS: Dict[List[str], str] = {
    ["1A", "1B", "2A", "2B", "3A"]: "\U0001FB1D",  # 🬝 - All except bottom-right
    ["1A", "1B", "2A", "2B", "3B"]: "\U0001FB2C",  # 🬬 - All except bottom-left
    ["1A", "1B", "2A", "3A", "3B"]: "\U0001FB34",  # 🬴 - All except middle-right
    ["1A", "2B", "2B", "3A", "3B"]: "\U0001FB38",  # 🬸 - All except middle-left
    ["1A", "2A", "2B", "3A", "3B"]: "\U0001FB3A",  # 🬺 - All except top-right
    ["1B", "2A", "2B", "3A", "3B"]: "\U0001FB3B",  # 🬻 - All except top-left
}

SIX_CELLS: Dict[List[str], str] = {
    [
        "1A",
        "1B",
        "2A",
        "2B",
        "3A",
        "3B",
    ]: "\U0001FB8B",  # 🮋 - All cells filled (full block)
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

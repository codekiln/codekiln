import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Directory to store rendered glyphs
GLYPH_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "sextant_glyphs"
)
os.makedirs(GLYPH_DIR, exist_ok=True)

# Unicode range for Symbols for Legacy Computing Sextant glyphs
START_UNICODE = 0x1FB00
END_UNICODE = 0x1FB7F
GLYPH_SIZE = (48, 72)  # High-resolution rendering (multiples of 2×3)

# Load IBM 3270 font that supports these Unicode characters
FONT_PATH = os.path.expanduser("~/Library/Fonts/3270-Regular.ttf")  # IBM 3270 font
FONT_SIZE = 64  # Adjusted for clarity


def render_glyph_to_image(char, save_path):
    """Render a Unicode character to an image file."""
    img = Image.new("L", GLYPH_SIZE, "white")  # White background
    draw = ImageDraw.Draw(img)

    # Load font
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"Font not found: {FONT_PATH}, using default.")
        font = ImageFont.load_default()

    # Get size and position to center the character
    text_size = draw.textbbox((0, 0), char, font=font)
    text_x = (GLYPH_SIZE[0] - text_size[2]) // 2
    text_y = (GLYPH_SIZE[1] - text_size[3]) // 2

    # Draw the character in black
    draw.text((text_x, text_y), char, font=font, fill="black")

    # Check if the glyph was actually rendered (not just a blank square)
    # by counting non-white pixels
    img_array = np.array(img)
    if np.sum(img_array < 240) < 10:  # If fewer than 10 non-white pixels
        # Try to create a synthetic glyph based on the Unicode value
        # For sextants, we can create a 2x3 grid with appropriate cells filled
        synthetic_img = create_synthetic_sextant(char)
        if synthetic_img is not None:
            img = synthetic_img

    # Save image
    img.save(save_path)
    return img


def create_synthetic_sextant(char):
    """Create a synthetic sextant glyph if the font doesn't support it."""
    if ord(char) < START_UNICODE or ord(char) > END_UNICODE:
        return None

    # Create a blank image
    img = Image.new("L", GLYPH_SIZE, "white")
    draw = ImageDraw.Draw(img)

    # Sextants are 2x3 grids, with bits representing which cells are filled
    # The bits are ordered from top-left to bottom-right, row by row
    code_point = ord(char)
    offset = code_point - START_UNICODE

    # Calculate cell size
    cell_width = GLYPH_SIZE[0] // 2
    cell_height = GLYPH_SIZE[1] // 3

    # Draw filled cells based on the bits in the code point
    for i in range(6):
        if (offset >> i) & 1:
            row = i // 2
            col = i % 2
            x0 = col * cell_width
            y0 = row * cell_height
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            draw.rectangle([x0, y0, x1, y1], fill="black")

    return img


# Render all sextant glyphs
glyph_data = {}
for code in range(START_UNICODE, END_UNICODE + 1):
    char = chr(code)
    save_path = os.path.join(GLYPH_DIR, f"{code}.png")
    try:
        img = render_glyph_to_image(char, save_path)

        # Convert image to binary (black/white) grid
        binary_grid = np.array(img.convert("1")).astype(int)  # 0 = white, 1 = black
        glyph_data[char] = binary_grid
    except Exception as e:
        print(f"Warning: Could not render glyph {code:X} ({char}): {e}")

print(f"✅ Rendered and stored {len(glyph_data)} sextant glyphs.")

# Save paths to the images for verification
glyph_image_paths = list(glyph_data.keys())
glyph_image_paths[:10]  # Show first 10 glyphs


def match_gol_grid_to_glyph(game_grid):
    """
    Given a high-resolution Game of Life frame, find the best matching Unicode glyph.
    """
    best_match = None
    min_distance = float("inf")

    for char, glyph_grid in glyph_data.items():
        # Ensure game_grid is the same size as the glyph grid
        if game_grid.shape != glyph_grid.shape:
            continue  # Skip mismatched sizes

        # Compute Euclidean distance between binary grids
        distance = np.sum((game_grid - glyph_grid) ** 2)

        if distance < min_distance:
            min_distance = distance
            best_match = char

    return best_match


# Example: Convert a Life grid into sextant glyphs
def render_life_grid_to_sextants(life_grid):
    """
    Converts a Conway's Game of Life grid into sextant Unicode glyphs.
    """
    h, w = life_grid.shape
    output = []

    for y in range(0, h, GLYPH_SIZE[1] // 6):  # Step through 6-pixel chunks
        row_chars = []
        for x in range(0, w, GLYPH_SIZE[0] // 2):  # Step through 2-pixel chunks
            block = life_grid[y : y + 6, x : x + 2]
            best_char = match_gol_grid_to_glyph(block)
            row_chars.append(best_char or "🮀")  # Default to empty space if no match
        output.append("".join(row_chars))

    return "\n".join(output)


# Generate a test Life grid and render it
life_grid = np.random.choice([0, 1], size=(72, 36), p=[0.7, 0.3])
unicode_output = render_life_grid_to_sextants(life_grid)

print("Game of Life Frame (Rendered as Unicode Characters):")
print(unicode_output)

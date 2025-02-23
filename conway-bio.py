#!/usr/bin/env python3
import os
import sys
import getpass
import requests

# Only try to load dotenv if not running in GitHub Actions
if "GITHUB_ACTIONS" not in os.environ:
    from dotenv import load_dotenv

    load_dotenv()

LIVE = "■"
DEAD = "□"
ROWS = 8
COLS = 18


def main():
    # Read PAT from environment variable "PAT_GITHUB"
    pat = os.getenv("PAT_GITHUB")
    if not pat:
        # Fall back to prompt if not set, without echoing the input.
        pat = getpass.getpass("Enter your GitHub PAT (it will not be echoed): ")

    # 1) GET /user to read current bio
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {pat}",
    }
    response = requests.get("https://api.github.com/user", headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch user data: {response.status_code} {response.text}")
        sys.exit(1)

    user_data = response.json()
    current_bio = user_data.get("bio") or ""

    # 2) Parse the first 8 lines of the bio as an 18x8 Conway board
    lines = current_bio.split("\n")
    board_lines = lines[:ROWS]  # Use the first 8 lines

    # Validate that we have 8 lines of exactly 18 characters
    valid = True
    if len(board_lines) < ROWS:
        valid = False
    else:
        for line in board_lines:
            if len(line) != COLS:
                valid = False
                break

    # If invalid, seed a default glider board
    if not valid:
        board_lines = [
            "□■□□□□□□□□□□□□□□□□",
            "□□■□□□□□□□□□□□□□□□",
            "■■■□□□□□□□□□□□□□□□",
            "□□□□□□□□□□□□□□□□□□",
            "□□□□□□□□□□□□□□□□□□",
            "□□□□□□□□□□□□□□□□□□",
            "□□□□□□□□□□□□□□□□□□",
            "□□□□□□□□□□□□□□□□□□",
        ]

    # Convert board_lines to a 2D boolean array (True=live, False=dead)
    board = []
    for line in board_lines:
        row = [(c == LIVE) for c in line]
        board.append(row)

    # 3) Evolve the board by one step
    def neighbors(r, c):
        cnt = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < ROWS and 0 <= cc < COLS:
                    if board[rr][cc]:
                        cnt += 1
        return cnt

    new_board = []
    for r in range(ROWS):
        new_row = []
        for c in range(COLS):
            live_n = neighbors(r, c)
            if board[r][c]:
                # Survives with 2 or 3 neighbors
                new_row.append(live_n in [2, 3])
            else:
                # Becomes alive with exactly 3 neighbors
                new_row.append(live_n == 3)
        new_board.append(new_row)

    # 4) Convert the new_board back to lines of ■/□
    next_lines = []
    for r in range(ROWS):
        line = "".join(LIVE if new_board[r][c] else DEAD for c in range(COLS))
        next_lines.append(line)

    new_bio = "\n".join(next_lines)

    # 5) PATCH /user to update the bio
    payload = {"bio": new_bio}
    patch_response = requests.patch(
        "https://api.github.com/user", headers=headers, json=payload
    )
    if patch_response.status_code != 200:
        print(
            f"Failed to update bio: {patch_response.status_code} {patch_response.text}"
        )
        sys.exit(1)

    print("Bio updated successfully!")
    print(new_bio)


if __name__ == "__main__":
    main()

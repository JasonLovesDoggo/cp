from manim import *
from typing import List

class SearchVisualization(Scene):
    def construct(self):
        # Input data
        raw_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

        # Prepare the data
        data = [list(row) for row in raw_data.splitlines()]

        # Create the grid with proper scaling
        square_size = 0.4
        grid = self.create_grid(data, square_size)

        # Center the grid and scale to fit the screen
        grid.center()
        grid.scale(min(config.frame_width / grid.width, config.frame_height / grid.height) * 0.9)

        self.add(grid)

        # Create text for tracking search progress
        search_text = Text("Searching...", font_size=24).to_edge(UP)
        self.add(search_text)

        # Create text for total matches
        match_text = Text("Matches: 0", font_size=24).next_to(search_text, DOWN)
        self.add(match_text)

        # Find and highlight XMAS patterns
        xmas_count = self.find_xmas_patterns(data, grid, square_size,
                                             search_text, match_text)

        # Update final count
        final_count_text = Text(f"Total XMAS Patterns Found: {xmas_count}",
                                font_size=24).to_edge(DOWN)
        self.play(
            FadeOut(search_text),
            FadeOut(match_text),
            Create(final_count_text)
        )
        self.wait(0.5)

    def create_grid(self, data: List[List[str]], square_size: float) -> VGroup:
        """Create a grid of squares with letters."""
        grid_size = len(data)
        grid = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                # Create square
                square = Square(side_length=square_size).shift(
                    RIGHT * j * square_size +
                    UP * i * square_size
                )
                # Create text
                text = Text(data[i][j], font_size=16).move_to(square)
                grid.add(square, text)
        return grid

    def find_xmas_patterns(self,
                           data: List[List[str]],
                           grid: VGroup,
                           square_size: float,
                           search_text: Text,
                           match_text: Text) -> int:
        """Find and highlight all XMAS patterns."""
        grid_size = len(data)
        xmas_count = 0

        # Directions to check: right, down, diagonal down-right, diagonal down-left
        directions = [
            # (delta row, delta col)
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal down-right
            (1, -1)   # diagonal down-left
        ]

        # Words to search for (both forward and backward)
        target_words = ["XMAS", "SAMX"]

        for word_index, word in enumerate(target_words):
            # Update search text for current word
            search_text.become(
                    Text(f"Searching for: {word}", font_size=24).to_edge(LEFT).to_edge(UP)
                )


            for i in range(grid_size):
                for j in range(grid_size):
                    # Create yellow highlight for current cell
                    current_cell_index = (i * grid_size + j) * 2
                    current_square = grid[current_cell_index]
                    highlight = SurroundingRectangle(current_square, color=YELLOW, buff=0.05)
                    # self.play(Create(highlight))
                    self.add(highlight)

                    for dr, dc in directions:
                        # Check if pattern fits within grid
                        if (0 <= i + dr * 3 < grid_size and
                                0 <= j + dc * 3 < grid_size):
                            # Check if current position matches pattern
                            if self.check_pattern(data, i, j, dr, dc, word):
                                # Highlight the pattern
                                pattern_squares = self.get_pattern_squares(
                                    grid, i, j, dr, dc, grid_size
                                )

                                # Create a green rectangle around the pattern
                                rectangle = VGroup(*[
                                    SurroundingRectangle(square, color=GREEN, buff=0.3)
                                    for square in pattern_squares
                                ])

                                # Increment and update match count
                                xmas_count += 1
                                self.play(
                                    Create(rectangle),
                                    match_text.animate.become(
                                        Text(f"Matches: {xmas_count}", font_size=24).next_to(search_text, DOWN)
                                    )
                                )

                                # Wait for 0.05 second to show the match
                                self.wait(0.05)

                                # Remove the rectangle
                                self.play(FadeOut(rectangle))
                    self.remove(highlight)

        return xmas_count

    def check_pattern(self, data: List[List[str]],
                      start_row: int,
                      start_col: int,
                      delta_row: int,
                      delta_col: int,
                      target_word: str) -> bool:
        """Check if a specific pattern exists."""
        for k in range(4):
            row = start_row + k * delta_row
            col = start_col + k * delta_col
            if data[row][col] != target_word[k]:
                return False
        return True

    def get_pattern_squares(self,
                            grid: VGroup,
                            start_row: int,
                            start_col: int,
                            delta_row: int,
                            delta_col: int,
                            grid_size: int) -> VGroup:
        """Get the VGroup of squares for a specific pattern."""
        pattern_squares = VGroup()
        for k in range(4):
            # Calculate index in the grid (remember grid contains both squares and text)
            row = start_row + k * delta_row
            col = start_col + k * delta_col
            grid_index = (row * grid_size + col) * 2 + 1  # +1 to get text
            pattern_squares.add(grid[grid_index])
        return pattern_squares

# To render the animation
if __name__ == "__main__":
    scene = SearchVisualization()
    scene.render()

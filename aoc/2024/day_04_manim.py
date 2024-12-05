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

        # Create NumberPlane instead of manual grid positioning
        plane = NumberPlane(
            x_range=[0, len(data[0]), 1],
            y_range=[0, len(data), 1],
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
                "stroke_opacity": 0.2
            }
        )
        self.add(plane)

        # Create the grid with proper scaling
        grid = self.create_grid(data)

        # Center the grid
        grid.center()

        # Scale to fit screen, with a bit of padding
        grid.scale(min(config.frame_width / grid.width, config.frame_height / grid.height) * 0.8)

        self.add(grid)

        # Create text for tracking search progress
        search_text = Text("Searching...", font_size=24).to_edge(UP).to_edge(LEFT)
        self.add(search_text)

        # Create text for total matches
        matches = Text("Matches: ", font_size=24).next_to(search_text, DOWN)
        self.add(matches)

        match_num = Integer(0, font_size=24).next_to(matches, RIGHT)
        self.add(match_num)

        # Find and highlight XMAS patterns
        xmas_count = self.find_xmas_patterns(data, grid,
                                             search_text, matches, match_num)

        # Update final count
        final_count_text = Text(f"Total XMAS Patterns Found: {xmas_count}",
                                font_size=24).to_edge(DOWN)
        self.play(
            FadeOut(search_text),
            Create(final_count_text)
        )
        self.wait(0.5)

    def create_grid(self, data: List[List[str]]) -> VGroup:
        """Create a grid of squares with letters."""
        grid = VGroup()
        for i, row in enumerate(reversed(data)):  # Reverse to match NumberPlane coordinates
            for j, letter in enumerate(row):
                # Create square
                square = Square(side_length=0.8).move_to(
                    RIGHT * j + UP * i
                )
                # Create text
                text = Text(letter, font_size=24).move_to(square)
                grid.add(square, text)
        return grid

    def find_xmas_patterns(self,
                           data: List[List[str]],
                           grid: VGroup,
                           search_text: Text,
                           matches: Text,
                           matches_num: Text) -> int:
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
            highlight = SurroundingRectangle(grid[0], color=YELLOW, buff=0.05)
            for i in range(grid_size):
                for j in range(grid_size):
                    # Create yellow highlight for current cell
                    current_cell_index = (i * grid_size + j) * 2
                    current_square = grid[current_cell_index]
                    self.play(highlight.animate.move_to(current_square.get_center()))

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

                                # Create a green polygon that connects the letters diagonally
                                pattern_vertices = [square.get_center() for square in pattern_squares]

                                # Rearrange vertices to create a polygon with diagonals
                                polygon_vertices = [
                                    pattern_vertices[0],
                                    pattern_vertices[1],
                                    pattern_vertices[3],
                                    pattern_vertices[2]
                                ]

                                pattern_polygon = Polygon(*polygon_vertices,
                                                          color=GREEN,
                                                          fill_opacity=0.2,
                                                          stroke_width=3)

                                # Increment and update match count
                                xmas_count += 1
                                self.play(
                                    Create(pattern_polygon),
                                    matches_num.animate.set_value(xmas_count)
                                )

                                # Wait for 0.05 second to show the match
                                self.wait(0.001)

                                # Remove the polygon
                                self.play(FadeOut(pattern_polygon))

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


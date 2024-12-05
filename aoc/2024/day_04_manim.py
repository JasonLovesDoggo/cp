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

        grid = self.create_grid(data)

        grid.center()

        # Scale to fit screen, with a bit of padding
        grid.scale(
            min(config.frame_width / grid.width, config.frame_height / grid.height)
            * 0.8
        )

        self.add(grid)

        # Create text for tracking search progress
        search_text = Text("Searching...", font_size=24).to_edge(UP).to_edge(LEFT)
        self.add(search_text)

        # Create text for total matches
        matches = Text("Matches: ", font_size=24).next_to(search_text, DOWN)
        self.add(matches)

        match_num = Integer(0, font_size=24).next_to(matches, RIGHT)
        self.add(match_num)

        xmas_count = self.find_xmas_patterns(
            data, grid, search_text, matches, match_num
        )

        final_count_text = Text(
            f"Total XMAS Patterns Found: {xmas_count}", font_size=24
        ).to_edge(DOWN)
        self.play(FadeOut(search_text), Create(final_count_text))
        self.wait(0.5)

    def create_grid(self, data: List[List[str]]) -> VGroup:
        """Create a grid of squares with letters."""
        grid = VGroup()
        for i, row in enumerate(data):
            for j, letter in enumerate(row):
                square = Square(side_length=0.8).move_to(
                    RIGHT * j + UP * i  # Uses UP * i for correct orientation
                )
                text = Text(letter, font_size=24).move_to(square)
                grid.add(square, text)
        return grid

    def find_xmas_patterns(
        self,
        data: List[List[str]],
        grid: VGroup,
        search_text: Text,
        matches: Text,
        matches_num: Text,
    ) -> int:
        """Find and highlight all XMAS patterns."""
        grid_size = len(data)
        xmas_count = 0

        directions = [
            # (delta row, delta col)
            (0, 1),  # horizontal
            (1, 0),  # vertical
            (1, 1),  # diagonal down-right
            (1, -1),  # diagonal down-left
        ]

        # Words to search for (both forward and backward)
        target_words = ["XMAS", "SAMX"]
        highlight = SurroundingRectangle(grid[0], color=YELLOW, buff=0.05)

        for word_index, word in enumerate(target_words):
            # Update search text for current word
            search_text.become(
                Text(f"Searching for: {word}", font_size=24).to_edge(LEFT).to_edge(UP)
            )
            for i in range(grid_size):
                for j in range(grid_size):
                    current_cell_index = (i * grid_size + j) * 2
                    current_square = grid[current_cell_index]
                    self.play(
                        highlight.animate.move_to(current_square.get_center()),
                        run_time=0.18,
                    )

                    for dr, dc in directions:
                        # Check if pattern fits within grid
                        if 0 <= i + dr * 3 < grid_size and 0 <= j + dc * 3 < grid_size:
                            # Check if current position matches pattern
                            if self.check_pattern(data, i, j, dr, dc, word):
                                # Highlight the pattern with a polygon (surrounding the squares)
                                pattern_squares = self.get_pattern_squares(
                                    grid, i, j, dr, dc, grid_size
                                )

                                # Get the corner points of the surrounding rectangles in the correct order
                                pattern_vertices = self.get_pattern_vertices(
                                    dr, dc, pattern_squares
                                )

                                # Create the polygon
                                pattern_polygon = Polygon(
                                    *pattern_vertices,
                                    color=GREEN,
                                    fill_opacity=0.2,
                                    stroke_width=3,
                                )

                                xmas_count += 1
                                self.play(
                                    Create(pattern_polygon),
                                    matches_num.animate.set_value(xmas_count),
                                )

                                pattern_polygon.set_opacity(0.3)

        return xmas_count

    def check_pattern(
        self,
        data: List[List[str]],
        start_row: int,
        start_col: int,
        delta_row: int,
        delta_col: int,
        target_word: str,
    ) -> bool:
        """Check if a specific pattern exists."""
        for k in range(4):
            row = start_row + k * delta_row
            col = start_col + k * delta_col
            if data[row][col] != target_word[k]:
                return False
        return True

    def get_pattern_squares(
        self,
        grid: VGroup,
        start_row: int,
        start_col: int,
        delta_row: int,
        delta_col: int,
        grid_size: int,
    ) -> VGroup:
        """Get the VGroup of squares for a specific pattern."""
        pattern_squares = VGroup()
        for k in range(4):
            row = start_row + k * delta_row
            col = start_col + k * delta_col
            grid_index = (row * grid_size + col) * 2
            pattern_squares.add(grid[grid_index])
        return pattern_squares

    def get_pattern_vertices(
        self, delta_row: int, delta_col: int, pattern_squares: List[Square]
    ) -> List[np.ndarray]:
        """Get the corner points of the surrounding rectangles in the correct order."""
        pattern_vertices = []

        if delta_row == 0:  # Horizontal
            pattern_vertices.extend(
                [
                    pattern_squares[0].get_corner(UL),
                    pattern_squares[3].get_corner(UR),
                    pattern_squares[3].get_corner(DR),
                    pattern_squares[0].get_corner(DL),
                ]
            )
        elif delta_col == 0:  # Vertical
            pattern_vertices.extend(
                [
                    pattern_squares[0].get_corner(DL),
                    pattern_squares[0].get_corner(DR),
                    pattern_squares[3].get_corner(UR),
                    pattern_squares[3].get_corner(UL),
                ]
            )
        # check if diaonally going right to left
        elif delta_col == -1:  # Diagonal left to right
            pattern_vertices.extend(
                [
                    pattern_squares[0].get_corner(UR),
                    pattern_squares[0].get_corner(DR),
                    pattern_squares[0].get_corner(DL),
                    pattern_squares[-1].get_corner(DL),
                    pattern_squares[-1].get_corner(UL),
                    pattern_squares[-1].get_corner(UR),
                ]
            )
        else:  # Diagonal Left to Right
            pattern_vertices.extend(
                [
                    pattern_squares[0].get_corner(DR),
                    pattern_squares[0].get_corner(DL),
                    pattern_squares[0].get_corner(UL),
                    pattern_squares[-1].get_corner(UL),
                    pattern_squares[-1].get_corner(UR),
                    pattern_squares[-1].get_corner(DR),
                ]
            )

        return pattern_vertices

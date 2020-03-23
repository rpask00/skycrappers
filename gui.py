import pygame


class Gui():
    def __init__(self):
        self.grid_lines = [
            [(0, 100), (800, 100)],
            [(0, 200), (800, 200)],
            [(0, 300), (800, 300)],
            [(0, 400), (800, 400)],
            [(0, 500), (800, 500)],
            [(0, 600), (800, 600)],
            [(0, 700), (800, 700)],

            [(100, 0), (100, 900)],
            [(200, 0), (200, 900)],
            [(300, 0), (300, 900)],
            [(400, 0), (400, 900)],
            [(500, 0), (500, 900)],
            [(600, 0), (600, 900)],
            [(700, 0), (700, 900)],
        ]

        self.GAME_FONT = GAME_FONT = pygame.freetype.Font("ArchivoNarrow-Bold.ttf", 45)

    def draw_lines(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface,  (132, 118, 0), line[0], line[1], 1)

    def write_clues(self, surface, clues):
        for i, c in enumerate(clues[:6]):
            if c is not 0:
                self.GAME_FONT.render_to(surface, (i*100+140, 40), str(c), (168, 150, 0))
            else:
                self.GAME_FONT.render_to(surface, (i*100+140, 40), str(c), (23, 21, 0))

        for i, c in enumerate(clues[6:12]):
            if c is not 0:
                self.GAME_FONT.render_to(surface, (750, i*100+140), str(c), (168, 150, 0))
            else:
                self.GAME_FONT.render_to(surface, (750, i*100+140), str(c), (23, 21, 0))

        for i, c in enumerate(clues[12:18]):
            if c is not 0:
                self.GAME_FONT.render_to(surface, ((5-i)*100+140, 750), str(c), (168, 150, 0))
            else:
                self.GAME_FONT.render_to(surface, ((5-i)*100+140, 750), str(c), (23, 21, 0))

        for i, c in enumerate(clues[18:]):
            if c is not 0:
                self.GAME_FONT.render_to(surface, (40, (5-i)*100+140), str(c), (168, 150, 0))
            else:
                self.GAME_FONT.render_to(surface, (40, (5-i)*100+140), str(c), (23, 21, 0))

    def draw_board(self, surface, id, row, city):
        pass
        for i, row in enumerate(city):
            for j, cell in enumerate(row):
                if cell is not 0:
                    self.GAME_FONT.render_to(surface, (j*100+140, i*100+140), str(cell), (255, 255, 255))
                else:
                    self.GAME_FONT.render_to(surface, (j*100+140, i*100+140), str(cell), (150, 0, 45))

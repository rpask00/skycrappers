import pygame.freetype  # Import the freetype module.
import copy
import functools
import itertools
import json
from gui import Gui
import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '-1260, 100'

pygame.init()
gui = Gui()
surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Skyscrappers')
programIcon = pygame.image.load('sk.png')
pygame.display.set_icon(programIcon)


class Puzzle():
    def __init__(self, clues):
        self.clues = clues
        self.perms = set(itertools.permutations([1, 2, 3, 4, 5, 6]))
        self.pairs = self.get_pairs()
        self.merged = []
        self.count = 0
        self.city = [[0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]

    def vertigo(self, prev, act):
        if act > prev[-1]:
            prev.append(act)
        return prev

    def print_city(self, city):
        print('-------------------------')
        for cc in city:
            print(cc)
        print('-------------------------')

    def get_Mutual(self, aa, bb):
        return list(set(aa).intersection(bb))

    def pygame_draw(self, id, row, city):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        surface.fill((0, 0, 0))
        gui.write_clues(surface, self.clues)
        gui.draw_lines(surface)
        gui.draw_board(surface, id, row, city)
        surface.set_alpha(1)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    def insert_row(self, id, row, city):
        self.pygame_draw(id, row, city)
        if id < 6:
            for i, r in enumerate(row):
                city[i][id] = r
            return city

        city[id - 6] = row
        cc = copy.deepcopy(city)
        return cc

    def chech_if_al_views_are_correct(self, city):
        inverse_city = []
        for i, c in enumerate(city):
            inverse_city.append([cc[i] for cc in city])
            if c.count(0):
                return False

            com = list(filter(lambda x: x['id'] == i + 6, self.merged))
            if com:
                com = com[0]['combinations']
                if not com.count(c):
                    return False

        for i, c in enumerate(inverse_city):
            if c.count(0):
                return False
            com = list(filter(lambda x: x['id'] == i, self.merged))
            if com:
                com = com[0]['combinations']
                if not com.count(c):
                    return False

        return True

    def get_pairs(self):
        views = [[] for x in range(6)]
        views_reverse = [[] for x in range(6)]
        for p in self.perms:
            point = list(p)
            inView = functools.reduce(self.vertigo, point, [point[0]])
            views[len(inView) - 1].append(json.dumps(point))
            point.reverse()
            views_reverse[len(inView) - 1].append(json.dumps(point))

        clues_1 = list(self.clues[:6])
        clues_2 = list(self.clues[6:12])
        clues_3 = list(self.clues[12:18])
        clues_3.reverse()
        clues_4 = list(self.clues[18:])
        clues_4.reverse()
        pairs = []

        for i, c in enumerate(clues_1):
            clues_1[i] = (clues_1[i], clues_3[i], i)

        for i, c in enumerate(clues_2):
            clues_2[i] = (clues_4[i], clues_2[i], i+6)

        for i, c in enumerate(clues_1 + clues_2):
            if not c[0] and not c[1]:
                pairs.append(None)
                continue
            elif c[0] and c[1]:
                mutual = self.get_Mutual(views[c[0]-1], views_reverse[c[1]-1])
            elif c[0] and not c[1]:
                mutual = views[c[0]-1]
            elif not c[0] and c[1]:
                mutual = views_reverse[c[1]-1]

            pairs.append({
                "is_horizontal": i > 5,
                "v1": c[0],
                "v2": c[1],
                "id": c[2],
                "combinations": [json.loads(m) for m in mutual],
                'size': len(mutual)
            })

        # return pairs[:6], pairs[6:]
        return pairs

    def validate_city(self, city, potential_row, index, is_horizontal):
        if is_horizontal:
            row = city[index]
        else:
            row = [c[index] for c in city]

        for i, r in enumerate(row):
            if r is 0:
                continue
            if r != potential_row[i]:
                return False

        return True

    def validate_city_all(self, city):
        reverse_city = [[] for x in range(6)]
        for row in city:

            for i, r in enumerate(row):
                reverse_city[i].append(r)

            if row.count(1) > 1 or row.count(2) > 1 or row.count(3) > 1 or row.count(4) > 1 or row.count(5) > 1 or row.count(6) > 1:
                return False

        for row in reverse_city:
            if row.count(1) > 1 or row.count(2) > 1 or row.count(3) > 1 or row.count(4) > 1 or row.count(5) > 1 or row.count(6) > 1:
                return False

        return True

    def solve_puzzle(self):
        combinations = list(filter(lambda i: i, self.pairs))
        self.merged = sorted(combinations, key=lambda x: x['size'])
        # self.merged = sorted(combinations, key=lambda x: len(x['combinations']))
        # self.valdate_two()
        self.solve(self.city, 0)
        return tuple([tuple(c) for c in self.city])

    def get_current_aligment(self, id, city):
        is_horizontal = id > 5

        if is_horizontal:
            return city[id % 6]

        row = []
        for c in city:
            row.append(c[id])

        return row

    def solve(self, city, id):
        self.count += 1
        if id == len(self.merged):
            if self.chech_if_al_views_are_correct(city):
                self.city = city
                return True
            else:
                self.solve_after(city)
                return True

        m = self.merged[id]

        current = self.get_current_aligment(m['id'], city)

        def filtr(row):
            for i, row in enumerate(row):
                if current[i] is 0:
                    continue

                if current[i] is not row:
                    return False

            return True

        # for c in m['combinations']:
        for c in filter(filtr, m['combinations']):
            # if self.validate_city(city, c, m['id'] % 6, m['is_horizontal']):
            fake_City = self.insert_row(m['id'], c, copy.deepcopy(city))
            # if not self.validate_city_all(fake_City):
            #     continue

            if self.solve(fake_City, id + 1):
                return True
        return False

    def solve_after(self, city):
        for i, c in enumerate(city):
            if c.count(0) is not 0:
                match = list(filter(lambda r: ((r[0] == c[0] or c[0] is 0) and (r[1] == c[1] or c[1] is 0) and (r[2] == c[2] or c[2] is 0) and (
                    r[3] == c[3] or c[3] is 0) and (r[4] == c[4] or c[4] is 0) and (r[5] == c[5] or c[5] is 0)), itertools.permutations([1, 2, 3, 4, 5, 6])))
                for m in match:
                    fake_City = self.insert_row(i+6, m, copy.deepcopy(city))
                    if not self.validate_city_all(fake_City):
                        continue

                    if self.solve_after(fake_City):
                        return True

        self.city = city
        return True

    def valdate_two(self):
        target1 = False
        target2 = False
        index1 = False
        index2 = False

        for i, m in enumerate(self.merged):
            if m['id'] < 6 and not target1:
                target1 = m
                index1 = i
            if m['id'] > 6 and not target2:
                target2 = m
                index2 = i

        ar1 = set()
        ar2 = set()
        for m1 in target1['combinations']:
            m1 = json.loads(m1)
            cici = self.insert_row(target1['id'], m1, copy.deepcopy(self.city))
            for m2 in target2['combinations']:
                if self.validate_city(cici, m2, target2['id'] % 6, target2['is_horizontal']):
                    ar1.add(str(m1))
                    ar2.add(str(m2))

        self.merged[index1]['combinations'] = [json.loads(a) for a in ar1]
        self.merged[index2]['combinations'] = [json.loads(a) for a in ar2]


clues = [
    # (3, 2, 2, 3, 2, 1,  1, 2, 3, 3, 2, 2,  5, 1, 2, 2, 4, 3,  3, 2, 1, 2, 2, 4),
    # (0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0),
    # (0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0),
    # (4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4),
    # (0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0),
    # (5, 4, 1, 2, 3, 4, 4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3),
    # (4, 4, 0, 3, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0),
    # (2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4, 4, 3, 2, 5, 1, 5),
    (1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4, 4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1),
    # (0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0, 0, 0, 0, 2, 2, 0),
    # (3, 2, 0, 3, 1, 0, 0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3),
    # (0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0, 0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1),
    # (0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0),
    # (0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0, 0, 3, 0, 5, 3, 4),
    # (5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4, 3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2),
    # (1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4, 3, 2, 2, 3, 2, 1),
    # (3, 2, 1, 2, 2, 4, 3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3),
    # (4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4),
    # (0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0),
    # (3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4)
]


puz = Puzzle(clues[0])
puz.solve_puzzle()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

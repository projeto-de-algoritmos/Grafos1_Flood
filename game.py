import pygame
import sys
import random
import math

# width and height of screen
size = (800, 600)
spacing = 80
starting_x = abs((((size[0] - 20) // spacing) * spacing) - size[0]) / 2
starting_y = abs((((size[1] - 20) // spacing) * spacing) - size[1]) / 2
# background color in rgb
color = (255, 255, 255)
node_color = (0, 0, 0)
player_color = (0, 255, 0)
clock = pygame.time.Clock()
rad = math.pi / 180

# initializing pygame library
pygame.init()

# setting screen size and background color
screen = pygame.display.set_mode(size)
screen.fill(color)

# setting program name and icon
pygame.display.set_caption("Flood Rush")
icon = pygame.image.load('wave.png')
pygame.display.set_icon(icon)


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.positions = dict()

    def add_nodes(self, node, pos):
        self.nodes.add(node)
        self.positions[pos] = node

    def update(self, player):
        for node in self.nodes:
            if player.position == (node.rect[0], node.rect[1]):
                pygame.draw.circle(screen, player.color, node.rect.center, 10)
                continue
            pygame.draw.circle(screen, node.color, node.rect.center, 10)


class Node(object):
    counter = 0

    def __init__(self):
        self.id = self.__class__.counter
        self.__class__.counter += 1
        self.rect = None
        self.color = node_color
        self.neighbors = set()


class Player(object):
    def __init__(self):
        self.color = player_color
        self.position = (random.randrange(starting_x, (((size[0] - 20) // spacing) * spacing), spacing),
                         random.randrange(starting_y, (((size[1] - 20) // spacing) * spacing), spacing))


def create_graph():
    pos = [starting_x, starting_y]
    graph = Graph()
    # will be used to connect nodes later on
    nodes = []
    while pos[1] <= size[1] - starting_y:
        node = Node()
        graph.add_nodes(node, (pos[0], pos[1]))
        nodes.append(node)
        node.rect = pygame.Rect(pos[0], pos[1], 20, 20)
        if pos[0] == size[0] - starting_x:
            pos[0] = starting_x
            pos[1] += spacing
            continue
        pos[0] += spacing

    pos = [starting_x, starting_y]
    for node in nodes:
        if pos[1] > size[1] - starting_y:
            break
        if pos[0] > size[0] - starting_x:
            pos[0] = starting_x
            pos[1] += spacing
        if pos[0] - spacing > 0:
            if not random.randint(0, 1):
                neighbor = graph.positions[pos[0] - spacing, pos[1]]
                node.neighbors.add(neighbor)
                arrow(screen, node_color, node_color, node.rect.center, (neighbor.rect.center[0]+15,
                                                                         neighbor.rect.center[1]), 5)
            '''if pos[1] - spacing > 0:
                if not random.randint(0, 2):
                    neighbor = graph.positions[pos[0] - spacing, pos[1] - spacing]
                    node.neighbors.add(neighbor)
                    arrow(screen, node_color, node_color, node.rect.center, (neighbor.rect.center[0] + 10,
                                                                             neighbor.rect.center[1] + 10), 5)'''
        if pos[0] + spacing < size[0]:
            if not random.randint(0, 1):
                neighbor = graph.positions[pos[0] + spacing, pos[1]]
                node.neighbors.add(neighbor)
                arrow(screen, node_color, node_color, node.rect.center, (neighbor.rect.center[0] - 15,
                                                                         neighbor.rect.center[1]), 5)
        if pos[1] - spacing > 0:
            if not random.randint(0, 1):
                neighbor = graph.positions[pos[0], pos[1] - spacing]
                node.neighbors.add(neighbor)
                arrow(screen, node_color, node_color, node.rect.center, (neighbor.rect.center[0],
                                                                         neighbor.rect.center[1] + 15), 5)
        if pos[1] + spacing < size[1]:
            if not random.randint(0, 1):
                neighbor = graph.positions[pos[0], pos[1] + spacing]
                node.neighbors.add(neighbor)
                arrow(screen, node_color, node_color, node.rect.center, (neighbor.rect.center[0],
                                                                         neighbor.rect.center[1] - 15), 5)

        pos[0] += spacing

    return graph


def arrow(scr, lcolor, tricolor, start, end, trirad, thickness=1):
    pygame.draw.line(scr, lcolor, start, end, thickness)
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
    pygame.draw.polygon(scr, tricolor, ((end[0] + trirad * math.sin(rotation),
                                         end[1] + trirad * math.cos(rotation)),
                                        (end[0] + trirad * math.sin(rotation - 120 * rad),
                                         end[1] + trirad * math.cos(rotation - 120 * rad)),
                                        (end[0] + trirad * math.sin(rotation + 120 * rad),
                                         end[1] + trirad * math.cos(rotation + 120 * rad))))


def main():
    graph = create_graph()
    player = Player()
    # main game loop will run as long as the user doesn't exit the program
    # all player interaction should be handled within this loop
    while True:
        graph.update(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x -= x % 20
                y -= y % 20
                player.position = x, y

        # update the display to present changes on screen
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

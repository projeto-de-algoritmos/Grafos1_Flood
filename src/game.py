import copy
import math
import random
import sys
import threading
import time

import colors
import pygame

# width and height of screen
size = (800, 600)
# space between nodes
spacing = 80
# compute x and y offset to avoid nodes spawning offscreen
starting_x = abs((((size[0] - 20) // spacing) * spacing) - size[0]) / 2
starting_y = abs((((size[1] - 20) // spacing) * spacing) - size[1]) / 2
# clock dictates how fast the screen is refreshed
clock = pygame.time.Clock()
# constant for arrow function
rad = math.pi / 180
# global variable used to ensure strong connectivity
strong_connected = False
# variable to ensure thread stops when program is closed
stop_thread = False

# initializing pygame library
pygame.init()

# setting screen size and background color
screen = pygame.display.set_mode(size)
screen.fill(colors.WHITE)

# setting program name and icon
pygame.display.set_caption("Flood Rush")
icon = pygame.image.load('images/wave.png')
menu = pygame.image.load('images/menu.png')
icon_big = pygame.transform.scale(icon, (80, 80))
pygame.display.set_icon(icon)

# game Win text
win_font = pygame.font.SysFont('comicsansms', 64)


def game_win_text():
    win_text = win_font.render("YOU WIN!", True, colors.BLUE)
    screen.blit(win_text, (250, 250))


def game_lose_text():
    win_text = win_font.render("YOU LOSE!", True, colors.EXIT)
    screen.blit(win_text, (250, 250))


def text_objects(text, font):
    text_surface = font.render(text, True, colors.NODE)
    return text_surface, text_surface.get_rect()


def button(msg, x, y, w, h, ic, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


def menu_game_window():
    menu_game = True

    while menu_game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        screen.fill(colors.WHITE)
        screen.blit(menu, (0, 0))

        # screen.fill(colors.WHITE)

        button('START', 350, 450, 100, 50, colors.BRIGHT_GREEN, game_loop)
        pygame.display.update()
        clock.tick(15)


def restart_game_window():
    restart_game = True

    while restart_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        button('RESTART', 250, 450, 100, 50, colors.GREEN, game_loop)
        button('QUIT', 450, 450, 100, 50, colors.EXIT, quit_game)

        pygame.display.update()
        clock.tick(15)


def quit_game():
    global stop_thread
    stop_thread = True
    pygame.quit()
    sys.exit()


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.positions = dict()

    def add_nodes(self, node, pos):
        self.nodes.add(node)
        # relate each node to it's position, used later for edge generation
        self.positions[pos] = node

    def update(self, player, out):
        for node in self.nodes:
            # draws flooded nodes
            if node.flooded:
                draw_circle(node, colors.FLOODED)
            # draws player node
            elif player.position == (node.rect[0], node.rect[1]):
                draw_circle(node, colors.PLAYER)
            # draws exit node
            elif out.position == (node.rect[0], node.rect[1]):
                draw_circle(node, colors.EXIT)
            # draws regular nodes
            else:
                draw_circle(node, colors.NODE)


class Node(object):
    counter = 0

    def __init__(self):
        self.id = self.__class__.counter
        self.__class__.counter += 1
        self.rect = None
        self.color = colors.NODE
        self.neighbours = set()
        self.flooded = False
        self.strong = False


class Player(object):
    def __init__(self):
        self.color = colors.PLAYER
        self.position = random_pos()


class Exit(object):
    def __init__(self):
        self.color = colors.EXIT
        self.position = random_pos()


def create_graph():
    pos = [starting_x, starting_y]
    graph = Graph()
    nodes = []
    # loop runs until bottom right corner of screen is reached
    # in pygame any given position within the screen is dictated by it's x, y coordinates
    # x and y both starts at 0 on the top left corner
    # x increases as you go right, y increases as you go down
    # meaning bottom right of the screen == screen size (screen variable)
    while pos[1] <= size[1] - starting_y:
        node = Node()
        # saves node + position on graph
        graph.add_nodes(node, (pos[0], pos[1]))
        nodes.append(node)
        # creates a Rect pygame object for each node
        # first two variables refers to object coordinates, last two refers to object size
        # this means that pygame actually sees each node as a 20 by 20 pixel square
        # they appear as circles because they are drawn as such on update() function
        node.rect = pygame.Rect(pos[0], pos[1], 20, 20)
        # guarantees there will be no nodes generating off screen
        if pos[0] == size[0] - starting_x:
            pos[0] = starting_x
            pos[1] += spacing
            continue
        pos[0] += spacing

    pos = [starting_x, starting_y]
    # loop to generate edges
    for node in nodes:
        # guarantees it won't go offscreen
        if pos[1] > size[1] - starting_y:
            break
        if pos[0] > size[0] - starting_x:
            pos[0] = starting_x
            pos[1] += spacing

            # following four if's verifies if there is a neighbouring node to the left, right, up and down respectively
            # for each given node
        if pos[0] - spacing > 0:
            # for example, if there is a neighbouring node to the left, it has a 50% chance of generating an edge
            # between the node and it's neighbour
            if random.randint(0, 1):
                # assigns neighbour node to variable neighbour
                neighbour = graph.positions[pos[0] - spacing, pos[1]]
                # add neighbour to node's list of neighbours
                node.neighbours.add(neighbour)
        if pos[0] + spacing < size[0]:
            if random.randint(0, 1):
                neighbour = graph.positions[pos[0] + spacing, pos[1]]
                node.neighbours.add(neighbour)
        if pos[1] - spacing > 0:
            if random.randint(0, 1):
                neighbour = graph.positions[pos[0], pos[1] - spacing]
                node.neighbours.add(neighbour)
        if pos[1] + spacing < size[1]:
            if random.randint(0, 1):
                neighbour = graph.positions[pos[0], pos[1] + spacing]
                node.neighbours.add(neighbour)

        pos[0] += spacing

    return graph


# main function to ensure strong connectivity
def strongly_connect(graph, rev_graph, start_pos):
    global strong_connected

    bfs(graph.positions[start_pos])
    bfs(rev_graph.positions[start_pos])

    update_strong_component(graph, rev_graph)

    # checks if the whole graph is strongly connected, returns if true
    for node in graph.nodes:
        if not node.strong:
            strong_connected = False
            break
        strong_connected = True

    if strong_connected:
        return

    fix_connectivity(graph, rev_graph)

    for node in graph.nodes:
        node.strong = False
        rev_graph.positions[node.rect[0], node.rect[1]].strong = False

    strongly_connect(graph, rev_graph, start_pos)


# reverse all edges of given graph
def reverse_graph(graph):
    rev_graph = copy.deepcopy(graph)
    for node in rev_graph.nodes:
        node.neighbours.clear()
    for node in graph.nodes:
        for neighbour in node.neighbours:
            rev_graph.positions[neighbour.rect[0], neighbour.rect[1]].neighbours.add(rev_graph.positions[node.rect[0],
                                                                                                         node.rect[1]])
    return rev_graph


# update nodes marked as strongly connected
def update_strong_component(graph, rev_graph):
    for node in graph.nodes:
        if node.strong and rev_graph.positions[node.rect[0], node.rect[1]].strong:
            continue
        else:
            node.strong = False


# fixes connectivity by generating edges between strongly connected component and other nodes
def fix_connectivity(graph, rev_graph):
    for node in graph.nodes:
        if not node.strong:
            if node.rect[0] - spacing > 0:
                if graph.positions[node.rect[0] - spacing, node.rect[1]].strong:
                    node.neighbours.add(graph.positions[node.rect[0] - spacing, node.rect[1]])
                    graph.positions[node.rect[0] - spacing, node.rect[1]].neighbours.add(node)
                    rev_graph.positions[node.rect[0], node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0] - spacing, node.rect[1]])
                    rev_graph.positions[node.rect[0] - spacing, node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1]])
                    return
            if node.rect[0] + spacing < size[0]:
                if graph.positions[node.rect[0] + spacing, node.rect[1]].strong:
                    node.neighbours.add(graph.positions[node.rect[0] + spacing, node.rect[1]])
                    graph.positions[node.rect[0] + spacing, node.rect[1]].neighbours.add(node)
                    rev_graph.positions[node.rect[0], node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0] + spacing, node.rect[1]])
                    rev_graph.positions[node.rect[0] + spacing, node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1]])
                    return
            if node.rect[1] - spacing > 0:
                if graph.positions[node.rect[0], node.rect[1] - spacing].strong:
                    node.neighbours.add(graph.positions[node.rect[0], node.rect[1] - spacing])
                    graph.positions[node.rect[0], node.rect[1] - spacing].neighbours.add(node)
                    rev_graph.positions[node.rect[0], node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1] - spacing])
                    rev_graph.positions[node.rect[0], node.rect[1] - spacing].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1]])
                    return
            if node.rect[1] + spacing < size[1]:
                if graph.positions[node.rect[0], node.rect[1] + spacing].strong:
                    node.neighbours.add(graph.positions[node.rect[0], node.rect[1] + spacing])
                    graph.positions[node.rect[0], node.rect[1] + spacing].neighbours.add(node)
                    rev_graph.positions[node.rect[0], node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1] + spacing])
                    rev_graph.positions[node.rect[0], node.rect[1] + spacing].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1]])
                    return


def bfs(node):
    node.strong = True
    queue = [node]

    while queue:
        s = queue.pop(0)

        for neighbour in s.neighbours:
            if not neighbour.strong:
                neighbour.strong = True
                queue.append(neighbour)


def draw_edges(graph):
    for node in graph.nodes:
        for neighbour in node.neighbours:
            if node.rect[0] > neighbour.rect[0]:
                arrow(screen, colors.NODE, colors.NODE, node.rect.center, (neighbour.rect.center[0] + 15,
                                                                           neighbour.rect.center[1]), 5)
            elif node.rect[0] < neighbour.rect[0]:
                arrow(screen, colors.NODE, colors.NODE, node.rect.center, (neighbour.rect.center[0] - 15,
                                                                           neighbour.rect.center[1]), 5)
            elif node.rect[1] < neighbour.rect[1]:
                arrow(screen, colors.NODE, colors.NODE, node.rect.center, (neighbour.rect.center[0],
                                                                           neighbour.rect.center[1] - 15), 5)
            elif node.rect[1] > neighbour.rect[1]:
                arrow(screen, colors.NODE, colors.NODE, node.rect.center, (neighbour.rect.center[0],
                                                                           neighbour.rect.center[1] + 15), 5)


# returns random position
def random_pos():
    return (random.randrange(starting_x, (((size[0] - 20) // spacing) * spacing), spacing),
            random.randrange(starting_y, (((size[1] - 20) // spacing) * spacing), spacing))


# draws circle on screen
def draw_circle(node, color):
    return pygame.draw.circle(screen, color, node.rect.center, 10)


# function to transform line to line with arrow
def arrow(scr, lcolor, tricolor, start, end, trirad, thickness=1):
    pygame.draw.line(scr, lcolor, start, end, thickness)
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
    pygame.draw.polygon(scr, tricolor, ((end[0] + trirad * math.sin(rotation),
                                         end[1] + trirad * math.cos(rotation)),
                                        (end[0] + trirad * math.sin(rotation - 120 * rad),
                                         end[1] + trirad * math.cos(rotation - 120 * rad)),
                                        (end[0] + trirad * math.sin(rotation + 120 * rad),
                                         end[1] + trirad * math.cos(rotation + 120 * rad))))


# flood function, runs until all reachable nodes are flooded or program is closed
def flood_fill(node):
    global stop_thread
    q = [node]
    while q:
        if stop_thread:
            break
        flooded = q.pop(0)
        flooded.flooded = True
        time.sleep(0.3)
        for neighbour in flooded.neighbours:
            if not neighbour.flooded:
                q.append(neighbour)


# ensures minimum distance between starting nodes
def min_dist(flood, player, out):
    while math.hypot(flood[0] - player.position[0], flood[1] - player.position[1]) < 300:
        player.position = random_pos()
    while math.hypot(flood[0] - out.position[0], flood[1] - out.position[1]) < 300 or math.hypot(
            player.position[0] - out.position[0], player.position[1] - out.position[1]) < 300:
        out.position = random_pos()


def game_loop():
    graph = create_graph()
    player = Player()
    out = Exit()
    rev_graph = reverse_graph(graph)
    strongly_connect(graph, rev_graph, player.position)
    draw_edges(graph)

    flood_pos = random_pos()
    min_dist(flood_pos, player, out)
    flood_node = graph.positions[flood_pos[0], flood_pos[1]]

    global stop_thread
    stop_thread = False
    x = threading.Thread(target=flood_fill, args=(flood_node,))
    x.start()

    # main game loop will run as long as the user doesn't exit the program
    # all player interaction should be handled within this loop
    while True:

        graph.update(player, out)

        if player.position == out.position:
            game_win_text()
            restart_game_window()
            quit_game()
        elif graph.positions[player.position].flooded or graph.positions[out.position].flooded:
            game_lose_text()
            restart_game_window()
            quit_game()

        # loop constantly reads for player interaction
        for event in pygame.event.get():
            # if the player presses the x button
            if event.type == pygame.QUIT:
                quit_game()
            # if the player presses any key
            if event.type == pygame.KEYDOWN:
                (x, y) = player.position
                if event.key == pygame.K_UP:
                    if (x, y - spacing) in graph.positions:
                        if graph.positions[x, y - spacing] in graph.positions[x, y].neighbours:
                            player.position = x, y - spacing
                elif event.key == pygame.K_DOWN:
                    if (x, y + spacing) in graph.positions:
                        if graph.positions[x, y + spacing] in graph.positions[x, y].neighbours:
                            player.position = x, y + spacing
                elif event.key == pygame.K_LEFT:
                    if (x - spacing, y) in graph.positions:
                        if graph.positions[x - spacing, y] in graph.positions[x, y].neighbours:
                            player.position = x - spacing, y
                elif event.key == pygame.K_RIGHT:
                    if (x + spacing, y) in graph.positions:
                        if graph.positions[x + spacing, y] in graph.positions[x, y].neighbours:
                            player.position = x + spacing, y

        # update the display to present changes on screen
        pygame.display.update()
        # clock is currently 60 frames per second
        clock.tick(60)


def main():
    menu_game_window()
    game_loop()


if __name__ == "__main__":
    main()

import pygame

# width and height of screen
size = (800, 600)
spacing = 80
starting_x = abs((((size[0]-20)//spacing) * spacing) - size[0]) / 2
starting_y = abs((((size[1]-20)//spacing) * spacing) - size[1]) / 2
# background color in rgb
color = (255, 255, 255)
node_color = (0, 0, 255)

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

    def add_nodes(self, node):
        self.nodes.add(node)

    def update(self):
        for node in self.nodes:
            pygame.draw.circle(screen, node.color, node.rect.center, 10)


class Node(object):
    counter = 0

    def __init__(self):
        self.id = self.__class__.counter
        self.__class__.counter += 1
        self.rect = None
        self.color = node_color
        self.neighbors = set()


def create_graph():
    pos = [starting_x, starting_y]
    graph = Graph()
    # will be used to connect nodes later on
    nodes = []
    while pos[1] <= size[1]-starting_y:
        node = Node()
        graph.add_nodes(node)
        nodes.append(node)
        node.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        if pos[0] == size[0]-starting_x:
            pos[0] = starting_x
            pos[1] += spacing
            continue
        pos[0] += spacing

    return graph


def main():
    running = True
    graph = create_graph()
    # main game loop will run as long as the user doesn't exit the program
    # all player interaction should be handled within this loop
    while running:
        graph.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False

        # update the display to present changes on screen
        pygame.display.update()


if __name__ == "__main__":
    main()

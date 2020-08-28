import pygame

# width and height of screen
size = (800, 600)
# background color in rgb
color = (0, 0, 0)

# initializing pygame library
pygame.init()

# setting screen size and background color
screen = pygame.display.set_mode(size)
screen.fill(color)

# setting program name and icon
pygame.display.set_caption("Flood Rush")
icon = pygame.image.load('wave.png')
pygame.display.set_icon(icon)


def main():
    running = True
    # main game loop will run as long as the user doesn't exit the program
    # all player interaction should be handled within this loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # update the display to present changes on screen
        pygame.display.update()


if __name__ == "__main__":
    main()
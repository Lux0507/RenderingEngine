import pygame

class Point:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z
    # def __init__(self, coordinates):
    #     if len(coordinates) != 3:
    #         raise ValueError()
    #     self.X = coordinates[0]
    #     self.Y = coordinates[1]
    #     self.Z = coordinates[2]
    def project(self) -> list:
        return [
            self.X/self.Z, # x component of projected point
            self.Y/self.Z  # y component of projected point
        ]

SCREENSIZE = 500

# points beyond (SCREENSIZE, SCREENSIZE, 1)
# (-SCREENSIZE, SCREENSIZE, 1)
# (SCREENSIZE, -SCREENSIZE, 1)
# (-SCREENSIZE, -SCREENSIZE, 1)
# and beyond the pyramid formed by the upper coordinates with the origin arent displayed on the screen
points: list[Point] = []
points.append(Point(300, 300, 1))
points.append(Point(-300, 300, 1))
points.append(Point(300, 300, 4))
points.append(Point(-300, 300, 4))
points.append(Point(300, -300, 1))
points.append(Point(-300, -300, 1))
points.append(Point(300, -300, 4))
points.append(Point(-300, -300, 4))

# init pygame
pygame.init()
background = pygame.display.set_mode((500, 500))

# Screen, on wich to draw , which is being resized...
screen = pygame.Surface((SCREENSIZE, SCREENSIZE))
clock = pygame.time.Clock()
running = True

# draw on screen.
projected_points = []
for point in points:
    p = []
    for co in point.project():  # move (0, 0) to middle of screen
        p.append(co + SCREENSIZE/2)
    projected_points.append(p) 
    projected_points[-1][1] = -projected_points[-1][1] + SCREENSIZE # invert y
for point in projected_points:
    screen.fill((255, 255, 255), (point, (4,4))) # Changing the size of the rectangle to fill changes the size of the dot

# draw screen on background
background.blit(pygame.transform.scale(screen, background.get_rect().size), (0, 0))
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)
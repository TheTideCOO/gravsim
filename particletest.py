import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
G = 6.67430e-11  # gravitational constant

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Particle:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = 0
        self.vy = 0

    def apply_force(self, fx, fy, dt):
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * dt
        self.vy += ay * dt

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 5)

def compute_gravitational_force(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    r = math.sqrt(dx ** 2 + dy ** 2)
    if r == 0:
        return 0, 0
    force = G * p1.mass * p2.mass / (r ** 2)
    fx = force * dx / r
    fy = force * dy / r
    return fx, fy

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Gravity Simulation")
    clock = pygame.time.Clock()

    particles = []
    running = True

    while running:
        screen.fill(BLACK)
        dt = clock.tick(60) / 1000.0  # dt in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    particles.append(Particle(event.pos[0], event.pos[1], 1000))
                elif event.button == 3:  # Right mouse button
                    particles.append(Particle(event.pos[0], event.pos[1], 500))

        for p in particles:
            for other in particles:
                if p != other:
                    fx, fy = compute_gravitational_force(p, other)
                    p.apply_force(fx, fy, dt)

            p.update_position(dt)
            p.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

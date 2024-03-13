import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 800, 600
G = 0.4  # gravitational constant
PARTICLE_COUNT = 20
PARTICLE_RADIUS = 5
PARTICLE_SPEED = 5
SPLIT_THRESHOLD = 10  # Threshold size for splitting particles upon collision
BOUNCE_DAMPING = 0.8  # Damping factor for particle bounce

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Particle:
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), PARTICLE_RADIUS)

    def check_boundary_collision(self):
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -BOUNCE_DAMPING
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -BOUNCE_DAMPING

def compute_gravitational_force(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    r = max(math.sqrt(dx ** 2 + dy ** 2), 1)  # Ensure we don't divide by zero
    force = G / (r ** 2)
    fx = force * dx / r
    fy = force * dy / r
    return fx, fy

def check_collision(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance <= PARTICLE_RADIUS * 2:
        return True
    return False

def split_particle(p):
    # Split particle into smaller particles
    particles.remove(p)
    for _ in range(2):
        vx = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        vy = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        particles.append(Particle(p.x, p.y, vx, vy, p.mass / 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Simulation")
    clock = pygame.time.Clock()

    particles = []
    for _ in range(PARTICLE_COUNT):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        vx = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        vy = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        mass = random.uniform(1, 5)  # Random mass for each particle
        particles.append(Particle(x, y, vx, vy, mass))

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for p in particles:
            for other in particles:
                if p != other:
                    fx, fy = compute_gravitational_force(p, other)
                    p.apply_force(fx, fy)

            p.update_position()
            p.check_boundary_collision()
            p.draw(screen)

            # Check for collisions and split particles if necessary
            for other in particles:
                if p != other and check_collision(p, other):
                    if p.mass >= SPLIT_THRESHOLD:
                        split_particle(p)

        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

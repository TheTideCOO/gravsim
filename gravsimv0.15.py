import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 1500, 1100
G = 0.4  # gravitational constant
PARTICLE_COUNT = 250
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
        angle = random.uniform(0, 2 * math.pi)  # Random angle for initial velocity
        speed = random.uniform(0.5, 1.5) * PARTICLE_SPEED  # Random speed factor
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        particles.append(Particle(p.x, p.y, vx, vy, p.mass / 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GravSim v0.15")
    clock = pygame.time.Clock()

    particles = []
    for _ in range(PARTICLE_COUNT):
        x = random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS)
        y = random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)
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
        for p1 in particles:
            for p2 in particles:
                if p1 != p2 and check_collision(p1, p2):
                    if p1.mass >= SPLIT_THRESHOLD and p2.mass >= SPLIT_THRESHOLD:
                        split_particle(p1)
                        split_particle(p2)

        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

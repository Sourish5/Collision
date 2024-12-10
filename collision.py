#Input format : --particles n ... xr yr vxr vyr mr r g b ...

import argparse
import pygame
import numpy as np

class Particle:
    def __init__(self, position, velocity, mass, color):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.mass = mass
        self.color = color
        self.radius = np.pi * (mass ** 0.5)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, int(self.radius))

    def update_position(self, dt):
        self.position += self.velocity * dt

    def handle_wall_collision(self):
        if self.position.x - self.radius < 0 or self.position.x + self.radius > SCREEN_WIDTH:
            self.velocity.x = -self.velocity.x
        if self.position.y - self.radius < 0 or self.position.y + self.radius > SCREEN_HEIGHT:
            self.velocity.y = -self.velocity.y

        self.position.x = np.clip(self.position.x, self.radius, SCREEN_WIDTH - self.radius)
        self.position.y = np.clip(self.position.y, self.radius, SCREEN_HEIGHT - self.radius)


def resolve_collision(p1, p2):
    relative_position = p2.position - p1.position
    distance_squared = relative_position.magnitude_squared()

    if relative_position.magnitude() < p1.radius + p2.radius:
        relative_velocity = p1.velocity - p2.velocity
        velocity_dot = relative_velocity.dot(relative_position) / distance_squared
        impulse = 2 * velocity_dot / (1 / p1.mass + 1 / p2.mass)

        p1.velocity -= impulse * relative_position / p1.mass
        p2.velocity += impulse * relative_position / p2.mass


def parse_arguments():
    parser = argparse.ArgumentParser(description="2D Particle Collision Simulator")
    parser.add_argument(
        "--particles",
        type=int,
        required=True,
        help="Number of particles to simulate."
    )
    parser.add_argument(
        "--details",
        type=str,
        nargs="+",
        required=True,
        help="Details of particles: x,y,vx,vy,mass,color(r,g,b). Repeat for each particle."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    num_particles = args.particles
    details = args.details

    if len(details) != num_particles * 7:
        print("Invalid number of particle details. Each particle requires 7 values: x, y, vx, vy, mass, r, g, b.")
        return

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Collision Simulator")
    clock = pygame.time.Clock()

    particles = []
    for i in range(num_particles):
        x, y, vx, vy, mass, r, g, b = map(float, details[i * 7: (i + 1) * 7])
        particles.append(Particle(position=(x, y), velocity=(vx, vy), mass=mass, color=(int(r), int(g), int(b))))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for particle in particles:
            particle.update_position(1 / FPS)
            particle.handle_wall_collision()

        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                resolve_collision(particles[i], particles[j])

        for particle in particles:
            particle.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    FPS = 144
    BACKGROUND_COLOR = (0, 0, 0)

    main()

import pygame
import numpy as np

# Particle Class
class Particle:
    def __init__(self, color, mass, position, velocity, acceleration, e_particle, e_walls):
        self.color = color
        self.mass = mass
        self.radius = np.pi * (mass ** 0.5)  # Radius proportional to sqrt of mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.e_particle = e_particle  # Restitution with other particles
        self.e_walls = e_walls        # Restitution with walls

# Simulation Parameters
space_x, space_y = 600, 600
fps = 144
background = (0, 0, 0)

# Initialize Particles
particles = [
    Particle((70, 255, 255), 20, pygame.Vector2(100, 200), pygame.Vector2(200, 500), pygame.Vector2(0, 0), 1, 1),
    Particle((255, 0, 255), 50, pygame.Vector2(200, 200), pygame.Vector2(-50, 60), pygame.Vector2(0, 0), 1, 1),
    Particle((120,120,120),40,pygame.Vector2(300,200),pygame.Vector2(100,-30),pygame.Vector2(0,0),1,1),
    Particle((70,80,120),40,pygame.Vector2(70,50),pygame.Vector2(10,-130),pygame.Vector2(0,0),1,1),
    Particle((120,100,120),40,pygame.Vector2(120,20),pygame.Vector2(70,-30),pygame.Vector2(0,0),1,1),
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode([space_x, space_y])
clock = pygame.time.Clock()
dt = 1 / fps
running = True

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background)

    # Draw Particles
    for particle in particles:
        pygame.draw.circle(screen, particle.color, particle.position, int(particle.radius))

    # Collision with Walls
    for particle in particles:
        if particle.position.x + particle.radius > space_x:
            particle.velocity.x *= -particle.e_walls
        if particle.position.x - particle.radius < 0:
            particle.velocity.x *= -particle.e_walls
        if particle.position.y + particle.radius > space_y:
            particle.velocity.y *= -particle.e_walls
        if particle.position.y - particle.radius < 0:
            particle.velocity.y *= -particle.e_walls

    # Collision Between Particles
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            if i < j:  # Avoid double-checking and self-collision
                rel_position = p2.position - p1.position
                if rel_position.magnitude() < (p1.radius + p2.radius):  # Collision detected
                    # Calculate new velocities (perfectly elastic collision)
                    rel_velocity = p2.velocity - p1.velocity
                    collision_normal = rel_position.normalize()
                    velocity_diff = np.dot(rel_velocity, collision_normal)
                    
                    if velocity_diff < 0:  # Only resolve if particles are moving towards each other
                        impulse = (2 * velocity_diff) / (p1.mass + p2.mass)
                        p1.velocity += impulse * p2.mass * collision_normal
                        p2.velocity -= impulse * p1.mass * collision_normal

    # Update Particle Positions and Velocities
    for particle in particles:
        particle.position += particle.velocity * dt
        particle.velocity += particle.acceleration * dt

    # Display Frame
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

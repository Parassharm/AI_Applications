import pygame
import random
import math
from collections import deque

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Cracker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (180, 50, 180)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE]

# Game settings
BUBBLE_RADIUS = 20
SHOOT_SPEED = 10
CANNON_LENGTH = 40
GRID_OFFSET = 50

class Bubble:
    def __init__(self, x, y, color, stuck=False):
        self.x = x
        self.y = y
        self.color = color
        self.radius = BUBBLE_RADIUS
        self.stuck = stuck

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)

    def move(self, angle):
        self.x += SHOOT_SPEED * math.cos(math.radians(angle))
        self.y -= SHOOT_SPEED * math.sin(math.radians(angle))

def create_grid(rows, cols):
    grid = []
    for row in range(rows):
        for col in range(cols):
            if random.random() > 0.3:  # 70% chance of a bubble
                x = GRID_OFFSET + col * (BUBBLE_RADIUS * 2 + 2)
                y = GRID_OFFSET + row * (BUBBLE_RADIUS * 2 + 2)
                if row % 2 == 1:
                    x += BUBBLE_RADIUS
                grid.append(Bubble(x, y, random.choice(COLORS), True))
    return grid

def find_connected_bubbles(bubble, bubbles):
    queue = deque()
    queue.append(bubble)
    connected = []
    visited = set()

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        connected.append(current)
        
        for neighbor in bubbles:
            if neighbor != current and neighbor.stuck:
                distance = math.dist((current.x, current.y), (neighbor.x, neighbor.y))
                if distance < BUBBLE_RADIUS * 2.1 and neighbor.color == current.color:
                    queue.append(neighbor)
    
    return connected

def main():
    clock = pygame.time.Clock()
    running = True
    angle = 90
    bubbles = create_grid(5, 10)
    shooting_bubble = None
    game_over = False

    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    angle = min(180, angle + 5)
                elif event.key == pygame.K_RIGHT:
                    angle = max(0, angle - 5)
                elif event.key == pygame.K_SPACE and not shooting_bubble and not game_over:
                    shooting_bubble = Bubble(WIDTH//2, HEIGHT-50, random.choice(COLORS))
        
        # Draw cannon
        end_x = WIDTH//2 + CANNON_LENGTH * math.cos(math.radians(angle))
        end_y = HEIGHT-50 - CANNON_LENGTH * math.sin(math.radians(angle))
        pygame.draw.line(screen, BLACK, (WIDTH//2, HEIGHT-50), (end_x, end_y), 5)
        
        # Update and draw bubbles
        for bubble in bubbles:
            bubble.draw()
        
        # Handle shooting bubble
        if shooting_bubble:
            shooting_bubble.move(angle)
            shooting_bubble.draw()
            
            # Check wall collision
            if shooting_bubble.x <= BUBBLE_RADIUS or shooting_bubble.x >= WIDTH - BUBBLE_RADIUS:
                angle = 180 - angle
                shooting_bubble.move(angle)
            
            # Check ceiling collision
            if shooting_bubble.y <= BUBBLE_RADIUS:
                shooting_bubble.stuck = True
                bubbles.append(shooting_bubble)
                shooting_bubble = None
            
            # Check bubble collision
            for bubble in bubbles:
                if bubble.stuck:
                    distance = math.dist((shooting_bubble.x, shooting_bubble.y), (bubble.x, bubble.y))
                    if distance < BUBBLE_RADIUS * 2:
                        shooting_bubble.stuck = True
                        bubbles.append(shooting_bubble)
                        connected = find_connected_bubbles(shooting_bubble, bubbles)
                        if len(connected) >= 3:
                            for b in connected:
                                bubbles.remove(b)
                        shooting_bubble = None
                        break
        
        # Check game over
        for bubble in bubbles:
            if bubble.y >= HEIGHT - BUBBLE_RADIUS:
                game_over = True
        
        if game_over:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, RED)
            screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 36))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
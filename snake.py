import pygame
import random
import sys

# --- basic setup ---
pygame.init()
pygame.mixer.init()

#--- setup screen ---
WIDTH, HEIGHT = 550, 550
CELL_SIZE = 30
FPS = 10 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cute Neon Snake 🐍✨")
clock = pygame.time.Clock()

# --- sound setup ---
sfx_eat = pygame.mixer.Sound('eat.wav')
sfx_gameover = pygame.mixer.Sound('gameover.wav')
# --- image setup ---
snake_head_img = pygame.image.load("snakehead.png")
snake_head_img = pygame.transform.scale(snake_head_img, (30, 30))
snake_icon = pygame.image.load("snake_icon.png").convert_alpha()


# COLORS
BLACK = (0, 0, 0)
SNAKE_COLOR = (255, 215, 0)  # GOLD
BODY_GOLD = (255, 230, 80)
FOOD_COLOR = (255, 120, 180) # pink pastel neon
GRID_COLOR = (40, 40, 40)
SCORE_COLOR = (255, 182, 193)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)
RED = (255, 80, 80)



font = pygame.font.SysFont("Comic Sans MS", 32)
small_font = pygame.font.Font(None, 40)

# --- show menu ---
def show_menu():
    global snake_icon 
    while True:
        screen.fill(BLACK)

        # Title
        title = font.render("Snake Game - Ngan Nghiem", True, YELLOW)
        start_text = small_font.render("Press S to Start", True, WHITE)
        quit_text = small_font.render("Press Q to Quit", True, RED)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 50))

        snake_icon = pygame.transform.scale(snake_icon, (64, 64)) 
        screen.blit(snake_icon, (WIDTH//2 - title.get_width()//2 - 60, HEIGHT//3 - 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # press S to Start
                    return "start"
                elif event.key == pygame.K_q:  # press Q to Quit
                    pygame.quit()
                    return "quit"


# --- class Snake & Food ---
class Snake:
    def __init__(self):
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)  # right
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        self.body.insert(0, new_head)

    def change_direction(self, new_dir):
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.direction = new_dir

    def check_collision(self):
        head = self.body[0]
        # đụng tường
        if (head[0] < 0 or head[0] * CELL_SIZE >= WIDTH or
                head[1] < 0 or head[1] * CELL_SIZE >= HEIGHT):
            return True
        # đụng thân
        if head in self.body[1:]:
            return True
        return False

    def draw(self):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if i == 0:
                screen.blit(snake_head_img, rect)  # đầu rắn = ảnh pixel art
            else:
                pygame.draw.rect(screen, BODY_GOLD, rect, border_radius=8)
        if i == 0:
            if self.direction == (1, 0):  #right
                rotated_head = snake_head_img
            elif self.direction == (-1, 0):  # left
                rotated_head = pygame.transform.flip(snake_head_img, True, False)
            elif self.direction == (0, -1):  # up
                rotated_head = pygame.transform.rotate(snake_head_img, 90)
            elif self.direction == (0, 1):   # down
                rotated_head = pygame.transform.rotate(snake_head_img, -90)
            screen.blit(rotated_head, rect)
        
        # Nếu không phải đầu thì vẽ thân rắn bình thường
        else:
            pygame.draw.rect(screen, BODY_GOLD, rect, border_radius=8)



class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        while True:
            pos = (random.randint(0, WIDTH // CELL_SIZE - 1),
                   random.randint(0, HEIGHT // CELL_SIZE - 1))
            if pos not in snake.body:
                return pos

    def draw(self):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE + 5, y * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.ellipse(screen, FOOD_COLOR, rect)


# --- setup game ---
choice = show_menu()
if choice == "quit":
    exit()

snake = Snake()
food = Food()
score = 0
game_over = False

# --- main loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((1, 0))
            elif event.key == pygame.K_r and game_over:
                # restart game
                snake = Snake()
                food = Food()
                score = 0
                game_over = False

    if not game_over:
        snake.move()

        # eat food
        if snake.body[0] == food.position:
            sfx_eat.play()
            score += 1
            snake.grow = True
            food = Food()
        

        # check collision
        if snake.check_collision():
            sfx_gameover.play()
            game_over = True

    # --- draw screen ---
    screen.fill(BLACK)

    # lưới nhẹ cho đẹp
    for i in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (i, 0), (i, HEIGHT))
        pygame.draw.line(screen, GRID_COLOR, (0, i), (WIDTH, i))

    food.draw()
    snake.draw()

    # scoring
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    screen.blit(score_text, (10, 10))

    if game_over:
        msg = font.render("GAME OVER! Press R to restart", True, (255, 100, 120))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 30))

    pygame.display.flip()
    clock.tick(FPS)

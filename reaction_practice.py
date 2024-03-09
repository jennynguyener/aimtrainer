import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Can You Aim?")

TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (255, 217, 192)
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("Arial", 24)

class Target:
  MAX_SIZE = 30
  GROWTH_RATE = 0.4
  COLOR = (140, 192, 222)

  def __init__(self, x, y):
      self.x = x
      self.y = y
      self.size = 0
      self.grow = True

  def update(self):
    if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
      self.grow = False

    if self.grow:
      self.size += self.GROWTH_RATE
    else:
      self.size -= self.GROWTH_RATE * 2

  def draw(self, win):
    pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size) 

  def collide(self, x, y):
    dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
    return dis <= self.size

def draw(win, targets):
  win.fill(BG_COLOR)

  for target in targets:
    target.draw(win)


def format_time(secs):
  seconds = int(round(secs % 60, 1))

  return f"{seconds:02d}"


def draw_top_bar(win, elapsed_time, targets_pressed, misses):
  pygame.draw.rect(win, (231, 206, 166), (0, 0, WIDTH, TOP_BAR_HEIGHT))
  time_label = LABEL_FONT.render(
    f"Time: {format_time(elapsed_time)}", 1, "black")
  
  speed = round(targets_pressed / elapsed_time, 1)
  speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
  hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

  win.blit(time_label, (15, 10))
  win.blit(speed_label, (get_middle(speed_label), 10))
  win.blit(hits_label, (700, 10))

def end_screen(win, elapsed_time, targets_pressed, clicks):
  win.fill(BG_COLOR)
  
  speed = round(targets_pressed / elapsed_time, 1)
  speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1,(136, 74, 57))
  hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1,(136, 74, 57))
  accuracy = targets_pressed
  if accuracy > 0:
    accuracy = round(targets_pressed / clicks * 100, 1)
  else:
    accuracy = 0.0
  accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1,(136, 74, 57))

  win.blit(speed_label, (get_middle(speed_label), 100))
  win.blit(hits_label, (get_middle(hits_label), 200))
  win.blit(accuracy_label, (get_middle(accuracy_label), 300))

  pygame.display.update()

  run = True
  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
        quit()

def get_middle(surface):
  return WIDTH / 2 - surface.get_width()/2

def main():
  run = True
  targets = []
  clock = pygame.time.Clock()

  targets_pressed = 0
  clicks = 0
  misses = 0
  start_time = time.time()

  pygame.time.set_timer(TARGET_EVENT, 500)

  while run:
    clock.tick(60)
    click = False
    mouse_pos = pygame.mouse.get_pos()
    elapsed_time = time.time() - start_time

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break

      if event.type == TARGET_EVENT:
        x = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, WIDTH - TARGET_PADDING)
        y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
        target = Target(x, y)
        targets.append(target)

      if event.type == pygame.MOUSEBUTTONDOWN:
        click = True
        clicks += 1

    for target in targets:
      target.update()
      
      if target.size <= 0:
        targets.remove(target)
        misses += 1

      if click and target.collide(*mouse_pos):
        targets.remove(target)
        targets_pressed += 1

    if elapsed_time >= 60:
      end_screen(WIN, elapsed_time, targets_pressed, clicks)


    draw(WIN, targets)
    draw_top_bar(WIN, elapsed_time, targets_pressed, misses )
    pygame.display.update()


  pygame.quit()

if __name__ == "__main__":
  main()

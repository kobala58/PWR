import pygame
import random 


background_colour = (0,0,0)
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fitts by jawa dewelopers')
screen.fill(background_colour)
pygame.display.flip()

running = True
sizes = [50,150,300]
dists = [50, 200]
sizes = random.shuffle(sizes)
dists = random.shuffle(dists)

size_cnt = 0
dist_cnt = 0

def draw_rect():

    pygame.draw.rect(screen, (255,0,0), pygame.Rect(left, top, sizes[size_cnt], sizes[size_cnt]))


while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

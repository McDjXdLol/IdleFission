import pygame
import sys
import time

pygame.init()
screen = pygame.display.set_mode((1020, 950))
pygame.display.set_caption("Clickyer")

image = pygame.image.load("reactor.png").convert_alpha()
image = pygame.transform.scale(image, (400, 400))
x, y = 200, 100
rect = image.get_rect(topleft=(x, y))

font = pygame.font.SysFont(None, 15)
font_big = pygame.font.SysFont(None, 60)

jump_height = 10
jumping = False
jump_offset = 0
jump_speed = 4
going_up = True

clock = pygame.time.Clock()

points = 0
click_multiplier = 1

last_idle_time = time.time()
idle_income = 0

upgrades = [
    {"name": "Tiny Reactor Boost", "cost": 5, "click_mult": 1, "idle": 0},
    {"name": "Small Capacitor", "cost": 15, "click_mult": 2, "idle": 0},
    {"name": "Heat Sink", "cost": 30, "click_mult": 0, "idle": 1},
    {"name": "Power Amplifier", "cost": 50, "click_mult": 3, "idle": 0},
    {"name": "Quantum Flux", "cost": 80, "click_mult": 0, "idle": 3},
    {"name": "Nano Circuit", "cost": 120, "click_mult": 4, "idle": 0},
    {"name": "Superconductor", "cost": 170, "click_mult": 0, "idle": 5},
    {"name": "Particle Accelerator", "cost": 230, "click_mult": 5, "idle": 0},
    {"name": "Dark Matter Collector", "cost": 300, "click_mult": 0, "idle": 10},
    {"name": "Plasma Converter", "cost": 380, "click_mult": 6, "idle": 0},
    {"name": "Fusion Core", "cost": 470, "click_mult": 0, "idle": 15},
    {"name": "Antimatter Storage", "cost": 570, "click_mult": 8, "idle": 0},
    {"name": "Graviton Emitter", "cost": 680, "click_mult": 0, "idle": 20},
    {"name": "Chrono Stabilizer", "cost": 800, "click_mult": 10, "idle": 0},
    {"name": "Dimensional Rift", "cost": 930, "click_mult": 0, "idle": 30},
    {"name": "Energy Matrix", "cost": 1070, "click_mult": 12, "idle": 0},
    {"name": "Singularity Reactor", "cost": 1220, "click_mult": 0, "idle": 40},
    {"name": "Neutrino Collector", "cost": 1380, "click_mult": 15, "idle": 0},
    {"name": "Omega Core", "cost": 1550, "click_mult": 0, "idle": 50},
    {"name": "Eternity Engine", "cost": 1730, "click_mult": 20, "idle": 0},
]

upgrade_levels = [0] * len(upgrades)

def draw_panel():
    panel_rect = pygame.Rect(800, 0, 200, 660)
    pygame.draw.rect(screen, (40, 40, 40), panel_rect)

    title_surf = font_big.render("Upgrades", True, (255, 255, 255))
    screen.blit(title_surf, (810, 10))

    y_offset = 70
    for i, upgrade in enumerate(upgrades):
        cost = upgrade["cost"] + upgrade_levels[i] * (upgrade["cost"] // 2)  # cena rośnie o 50% co zakup
        name = upgrade["name"]
        text_color = (255, 255, 255) if points >= cost else (150, 150, 150)
        text = f"{name} - Cost: {cost} EP"
        text_surf = font.render(text, True, text_color)
        screen.blit(text_surf, (810, y_offset))

        level_surf = font.render(f"Lv: {upgrade_levels[i]}", True, (200, 200, 0))
        screen.blit(level_surf, (970, y_offset))

        y_offset += 30

def buy_upgrade(mouse_pos):
    global points, click_multiplier, idle_income

    if mouse_pos[0] < 800:
        return

    y_offset = 70
    for i, upgrade in enumerate(upgrades):
        cost = upgrade["cost"] + upgrade_levels[i] * (upgrade["cost"] // 2)
        rect = pygame.Rect(800, y_offset, 200, 30)
        if rect.collidepoint(mouse_pos):
            if points >= cost:
                points -= cost
                upgrade_levels[i] += 1
                click_multiplier += upgrade["click_mult"]
                idle_income += upgrade["idle"]
                print(f"Bought {upgrade['name']}! Click Multiplier: {click_multiplier}, Idle Income: {idle_income}")
            else:
                print("Not enough EP!")
            break
        y_offset += 30

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rect.collidepoint(event.pos) and not jumping:
                    points += click_multiplier
                    jumping = True
                    jump_offset = 0
                    going_up = True
                else:
                    buy_upgrade(event.pos)

    now = time.time()
    if now - last_idle_time >= 1:
        points += idle_income
        last_idle_time = now

    screen.fill((30, 30, 30))

    if jumping:
        if going_up:
            jump_offset += jump_speed
            if jump_offset >= jump_height:
                jump_offset = jump_height
                going_up = False
        else:
            jump_offset -= jump_speed
            if jump_offset <= 0:
                jump_offset = 0
                jumping = False

    current_y = y - jump_offset

    text_surface = font_big.render(f"EP: {points}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(text_surface, text_rect)

    screen.blit(image, (x, current_y))
    rect.topleft = (x, current_y)

    draw_panel()

    pygame.display.update()
    clock.tick(60)

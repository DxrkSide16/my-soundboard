import pygame
pygame.init()

background_colour = (204, 204, 255)
button_color = (102, 178, 255)
hover_color = (51, 153, 255)
text_color = (255, 255, 255)
white_key_color = (255, 255, 255)
white_key_hover_color = (200, 200, 200)
white_key_pressed_color = (150, 150, 150)

screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Soundboard')

font = pygame.font.Font(None, 74)
title_font = pygame.font.Font(None, 120)
key_name_font = pygame.font.Font(None, 24)

background_image = pygame.image.load('bluebackground.jpeg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

home_icon = pygame.image.load('whitehouse.png')
home_icon = pygame.transform.scale(home_icon, (50, 50))
home_icon_rect = home_icon.get_rect(topleft=(10, 10))

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.text_surf = font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        pygame.draw.rect(screen, self.text_color, self.rect, 2)
        screen.blit(self.text_surf, self.text_rect)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Key:
    def __init__(self, x, y, width, height, color, hover_color, pressed_color, sound_file, name):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.sound = pygame.mixer.Sound(sound_file)
        self.name = name
        self.name_surf = key_name_font.render(self.name, True, (0, 0, 0))
        self.pressed = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.pressed:
            pygame.draw.rect(screen, self.pressed_color, self.rect)
        elif self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

        name_rect = self.name_surf.get_rect(center=self.rect.center)
        screen.blit(self.name_surf, name_rect)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.sound.play()
                self.pressed = True
                return True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False
        return False

def draw_title(screen, text, font, color, x, y):
    title_surf = font.render(text, True, color)
    title_rect = title_surf.get_rect(center=(x, y))
    screen.blit(title_surf, title_rect)

start_button = Button(505, 310, 200, 100, "Start", button_color, hover_color, text_color)
exit_button = Button(505, 450, 200, 100, "Exit", button_color, hover_color, text_color)

keys = []
num_keys = 14
key_width = 80
key_height = 250
gap = (screen_width - (num_keys * key_width)) // (num_keys + 1)
start_x = gap
start_y = screen_height - key_height - 20

for i in range(num_keys):
    sound_file = f'key{i+1:02d}.ogg'
    key_name = f'{i+1}'
    keys.append(Key(start_x + i * (key_width + gap), start_y, key_width, key_height, white_key_color, white_key_hover_color, white_key_pressed_color, sound_file, key_name))

on_main_screen = True
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if on_main_screen:
            if start_button.click(event):
                on_main_screen = False
            if exit_button.click(event):
                running = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if home_icon_rect.collidepoint(event.pos):
                    on_main_screen = True
                for key in keys:
                    key.click(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for key in keys:
                    key.click(event)

    screen.blit(background_image, (0, 0))

    if on_main_screen:
        draw_title(screen, "Soundboard", title_font, text_color, screen_width // 2, 150)
        start_button.draw(screen)
        exit_button.draw(screen)
    else:
        screen.blit(home_icon, home_icon_rect.topleft)
        for key in keys:
            key.draw(screen)

    pygame.display.flip()

pygame.quit()






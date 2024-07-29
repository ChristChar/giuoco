import pygame

def scrivirobebelle():
    input_text = ""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return input_text
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

def draw_text_within(surface, text, shape, font, color):
    words = text.split(" ")
    line = ""
    y = shape.top
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] <= shape.width:
            line = test_line
        else:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (shape.left, y))
            line = word + " "
            y += font.get_height()
    text_surface = font.render(line, True, color)
    surface.blit(text_surface, (shape.left, y))

def is_color_light(color):
    r, g, b = color
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return brightness > 0.5

def draw_rounded_rect(surface, color, rect, radius):
    if isinstance(rect, pygame.rect.Rect):
        x, y, width, height = rect.x, rect.y, rect.width, rect.height
    else:
        x, y, width, height = rect
    pygame.draw.rect(surface, color, (x + radius, y, width - 2 * radius, height))
    pygame.draw.rect(surface, color, (x, y + radius, width, height - 2 * radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius)
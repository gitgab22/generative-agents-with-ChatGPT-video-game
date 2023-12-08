import pygame
from datetime import datetime, timedelta

def get_time(start_time, duration_milliseconds):
    # Convert the start time to a datetime object
    start_time_obj = datetime.strptime(start_time, "%H:%M")

    # Calculate the end time by adding the duration in milliseconds
    end_time_obj = start_time_obj + timedelta(minutes=duration_milliseconds/1000)

    # Format the end time as a string in the HH:MM format
    end_time = end_time_obj.strftime("%H:%M")

    return end_time

def update_screen(time, screen_info):
    screen = screen_info['screen']
    font = screen_info['font']
    

    text = time
    white = (255, 255, 255)
    black = (0, 0, 0)
    # Get text surface and rectangle
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()

    # Set the position of the rectangle (top-left corner)
    text_rect.topleft = (10, 10)

    # Draw
    pygame.draw.rect(screen, white, text_rect)  # Draw the rectangle
    screen.blit(text_surface, text_rect.topleft)  # Draw the text on the rectangle

    pygame.display.update()
def loading_screen(screen_info):
    # loading in the middle of the screen
    screen = screen_info['screen']
    font = screen_info['font']
    

    text = "Loading..."
    white = (255, 255, 255)
    black = (0, 0, 0)
    # Get text surface and rectangle
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()

    # Set the position of the rectangle (middle of the screen)
    text_rect.center = (screen_info['screen_width']//2, screen_info['screen_height']//2)

    # Draw
    pygame.draw.rect(screen, black, text_rect)  # Draw the rectangle
    screen.blit(text_surface, text_rect.topleft)  # Draw the text on the rectangle

    pygame.display.update()
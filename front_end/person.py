import pygame
from back_end.useful_functions import get_duration

class Person(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=5):
        super().__init__()
        self.image = image
        self.image.convert_alpha()
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, y))
        self.current_task = None
        self.begin_execution = pygame.time.get_ticks()  # time when the execution begins
        self.execute_duration = 0  # duration of execution
        self.walk_duration = 0  # duration of walking
    def move(self, screen, commande=None, tile_width = 5, tile_height  = 5):
        x_move = 0
        y_move = 0

        if commande:
            if commande == 'UP':
                y_move -= tile_height
            elif commande == 'DOWN':
                y_move += tile_height
            elif commande == 'LEFT':
                x_move -= tile_width
            elif commande == 'RIGHT':
                x_move += tile_width
            else:
                pass
        else:
            pass
    
        self.rect.x += x_move
        self.rect.y += y_move

        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def execute(self, task, screen_info):
        font = screen_info['font']
        screen = screen_info['screen']
        tile_width = screen_info['tile_width']
        tile_height = screen_info['tile_height']
        scale_factor = screen_info['scale_factor']

        # set up colors
        black = (0, 0, 0)
        white = (255, 255, 255)

        agent_x = self.rect.x
        agent_y = self.rect.y

        # write text
        text_surface = font.render(task, True, black)
        
        # get text size
        text_width, text_height = font.size(task)

        # calculate text box position
        padding = 2.5 * scale_factor
        text_box_rect = pygame.Rect(agent_x + tile_width//2 - text_width//2 - padding, agent_y - text_height - padding * 2, text_width + padding * 2, text_height + padding * 2)

        # draw text box
        pygame.draw.rect(screen, white, text_box_rect)
        pygame.draw.rect(screen, black, text_box_rect, 2)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(text_surface, (agent_x + tile_width//2 - text_width//2 , agent_y - text_height - padding))
    
    def do(self,commends,screen_info):
        if self.current_task == None:
            commend = commends.pop(0)
            if commend[-1] == "STAY":
                self.begin_execution = pygame.time.get_ticks() # time when the execution begins
                self.execute_duration = (get_duration(commend[1],commend[2]) - self.walk_duration)*1000 # duration of execution
                self.execute(commend[0], screen_info)
                self.current_task = commend[0]
                self.walk_duration = 0
            else:
                self.move(screen_info['screen'],commend[-1],screen_info['tile_width'],screen_info['tile_height'])
            self.walk_duration += 0.25
        else:
            now = pygame.time.get_ticks()
            self.execute(self.current_task, screen_info)
            if now - self.begin_execution >= self.execute_duration:
                self.current_task = None
                self.walk_duration = 0
            
        
           
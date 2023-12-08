from agent import Agent
from front_end.person import Person
from environment import Environment
from multiprocessing import Process, Manager
import time
import pytmx
import pygame
from front_end.pygames_fonctions import *

# Continue the execution of the plan in the back end
def continue_run_back_end(shared_parameter, env, agent, initial_plan):
    print('---------- Back-end begin ---------- \n')
    for i in range(1, 5):
        # Create sub tasks for task_i and return them
        sub_plan_i = agent.create_sub_plan(i, env.map.get_localisations())

        task_i = initial_plan[f'task_{i}']
        print(f'---------- Executing task {i}: {task_i[0]}, {task_i[1]}, {task_i[2]} ---------- \n')

        # Execute sub tasks for task_i
        for j in range(1, len(sub_plan_i)+1):
            env.queue_of_configurations = shared_parameter
            
            key = f'sub_task_{j}'
            print(f'---------- Executing sub task {j}: {sub_plan_i[key][0]}, {sub_plan_i[key][1]}, {sub_plan_i[key][2]}, {sub_plan_i[key][3]}---------- \n')
            agent.execute_sub_task(start=sub_plan_i[key][0], end=sub_plan_i[key][1], localisation=sub_plan_i[key][2], task=sub_plan_i[key][3], environment=env)
            
            shared_parameter = env.queue_of_configurations
        
        

# Run the environment in the front end
def run_front_end(shared_parameter):
    print('---------- Front-end begin ---------- \n')

    # initialize pygame and create window
    pygame.init()
    clock = pygame.time.Clock() 
    debut = False # to know if the execution has begun
    debut_time = pygame.time.get_ticks() # time when the execution begins

    FPS = 4

    scale_factor = 2
    tile_width = 16 * scale_factor
    tile_height =  16 * scale_factor
    rows = 20
    cols = 20
    screen_width = tile_width * rows
    screen_height = tile_height * cols

    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption('Village Map')

    # set up fonts
    font = pygame.font.SysFont(None, tile_height // 2 )
    # set up screen_info
    screen_info = {
        'screen': screen,
        'font': font,
        'tile_width': tile_width,
        'tile_height': tile_height,
        'scale_factor': scale_factor,
        'screen_width': screen_width,
        'screen_height': screen_height
    }
    # set up colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    # load images
    bg_img = pygame.image.load('front_end/tiled map/map.png').convert_alpha()
    sc_bg_img = pygame.transform.scale(bg_img, (screen_width,screen_height))
    tiled_map = pytmx.load_pygame('front_end/tiled map/map.tmx')

    # load agents
    agents = []
    for obj in tiled_map.get_layer_by_name("agents"):
            agent_image = tiled_map.get_tile_image_by_gid(obj.gid)
            sc_agent_img = pygame.transform.scale(agent_image, (tile_width, tile_height))
            if agent_image:
                agents.append(Person(obj.x * scale_factor, obj.y * scale_factor, sc_agent_img, tile_height))

    # function for bg
    def draw_bg():
        screen.blit(sc_bg_img, (0,0))


    commands = shared_parameter
    
    # 游戏主循环
    running = True

    while running:

        clock.tick(FPS)
        if debut == False:
            while len(commands) < 10:
                loading_screen(screen_info)
            debut_time = pygame.time.get_ticks()
            debut = True


        draw_bg()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if len(commands) > 0:
            agents[0].do(commands, screen_info)
        time = pygame.time.get_ticks() - debut_time # time since the beginning of the execution
        time = get_time("07:00", time) # time in the format HH:MM")
        update_screen(time, screen_info)


        
    pygame.quit()

def main():
    # Start the simulation on two different processes running in parallel
    with Manager() as manager:
        
        # Initial set up of the environment and the agent
        env = Environment(min_equivalent_seconds=2)
        agent = Agent(id='agent1')
        env.map.case_details[agent.position[0], agent.position[1]]["agents"].add(agent)
        
        # Create the initial plan of the day
        initial_plan = agent.create_initial_plan()
        print('done')
        
        # Create a shared parameter between the two processes
        shared_parameter = manager.list()

        # Start the simulation on two different processes running in parallel
        process1 = Process(target=continue_run_back_end, args=(shared_parameter, env, agent, initial_plan))
        process2 = Process(target=run_front_end, args=(shared_parameter,))

        process1.start()
        process2.start()

        process1.join()
        process2.join()

if __name__ == "__main__":
    main()
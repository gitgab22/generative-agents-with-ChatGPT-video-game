

# move the agent by one step in the direction
def move(agent, direction, environment):
    '''
    input:  agent, direction, environment
    output: the agent moves by one step in the direction in the environment
    '''
    map = environment.map
    
    map.case_details[agent.position[0], agent.position[1]]["agents"].remove(agent)
    
    if direction == "UP":
        agent.position = (agent.position[0]-1, agent.position[1])
    elif direction == "DOWN":
        agent.position = (agent.position[0]+1, agent.position[1])
    elif direction == "RIGHT":
        agent.position = (agent.position[0], agent.position[1]+1)
    else:
        agent.position = (agent.position[0],agent.position[1]-1)
    
    map.case_details[agent.position[0], agent.position[1]]["agents"].add(agent)

# Get the direction from position1 to position2
def direction(position1, position2):
    '''
    input:  position1, position2
    output: direction (DOWN, UP, RIGHT, LEFT) from position1 to position2
    '''
    if position1[0] == position2[0]:
        if position1[1] == position2[1] + 1:
            return "LEFT"
        else:
            return "RIGHT"
    elif position1[1] == position2[1]:
        if position1[0] == position2[0]+1:
            return "UP"
        else:
            return "DOWN"
    else:
        return None

# Move the agent from its current position to the destination            
def move_agent_to(agent, destination, environment, step=1):
    '''
    input:  agent, destination, environment, step
    output: the agent moves from its current position to the destination in the environment
    '''

    # Get the path from the current position to the destination
    path = environment.map.find_path(agent.position, destination)
    
    # Move the agent to the destination localisation in the environment
    while len(path) > 0:
        # remove the previous event from the map (from case_details) because it is not relevant anymore
        if agent.current_event != None:
            environment.map.remove_event(agent.current_event, agent.position)
        
        # Get the direction from the current position to the next position (DOWN, UP, RIGHT, LEFT)
        direc = direction(agent.position, path.pop(0))
        
        # Move the agent by one step in the direction
        move(agent, direc, environment)
        
        # Create the event to be added to the map (to case_details)
        event = agent.name + " is walking"
        
        # Update current event
        agent.current_event = event
        
        # add the new event to the map (to case_details)
        environment.map.add_event(event, agent.position,environment.get_time())
        
        # Add the new event to the list of configurations to be displayed
        environment.num += 1
        environment.add_configuration_to_the_queue([event, direc])
        

# Execute the task [start, end, destination_localisation, task] in the environment
def execute_sub_task(agent, start, end, destination_localisation, task, environment):
    print("execute sub task")
    '''
    output:
    if the agent is already at the destination localisation:
        the agent performs the task
        the task is added to the queue of configuration
    else:
        the agent moves to the destination localisation
        the task is added to the queue of configuration
    '''
    
    map = environment.map
    current_localisation = map.get_current_localisation(agent)
    
    if current_localisation == destination_localisation:
        # remove the previous event from the map (from case_details) because it is not relevant anymore
        if agent.current_event != None:
            map.remove_event(agent.current_event, agent.position)
            
        # Update current event
        agent.current_event = f'{task}, {start}, {end}'
        
        # add the new event to the map (to case_details)
        map.add_event(agent.current_event, agent.position, environment.get_time())
        
        # Add the new event to the list of configurations to be displayed
        environment.num += 1
        environment.add_configuration_to_the_queue([task, start, end, 'STAY'])
        
        
    else:
        # Get the coordinates (x, y) of the destination localisation
        destinations = map.get_coordinates(destination_localisation)
        
        # Pick the first destination that is a road
        for x, y in destinations:
            if map.grid_roads[x, y] != 0:
                x_road = x
                y_road = y
                break
        
        # Move the agent to the destination localisation in the environment
        move_agent_to(agent, (x_road, y_road), environment)
        
        # remove the previous event from the map (from case_details) because it is not relevant anymore
        if agent.current_event != None:
            environment.map.remove_event(agent.current_event, agent.position)
                
        # Update current event
        agent.current_event = f'{task}, {start}, {end}'
        
        # add the new event to the map (to case_details)
        environment.map.add_event(agent.current_event, agent.position, environment.get_time())
        
        # Add the new event to the list of configurations to be displayed
        environment.num += 1
        environment.add_configuration_to_the_queue([task, start, end, 'STAY'])

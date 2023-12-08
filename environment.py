import time
from back_end.useful_functions import get_duration
from back_end.map.functions import find_path, nearby, get_current_localisation, prepare_map


class Map:
    def __init__(self):
       self.width, self.height, self.case_details, self.map_dict, self.coordinates, self.grid_roads, self.localisations = prepare_map()
    
    # Get case details
    def get_case_details(self, x, y):
        return self.case_details[x][y]
    
    # Get the localisation of the agent
    def get_current_localisation(self, agent):
        return get_current_localisation(self, agent)
        
    # Get the localisations of the map
    def get_localisations(self):
        return self.localisations
    
    # Get the coordinates of each place
    def get_coordinates(self, key):
        return self.coordinates[key]
    
    # Find a path from start to destination
    def find_path(self, start, destination):
        return find_path(self.grid_roads, start, destination)

    # get the events nearby the agent
    def nearby(self, position):
        return nearby(self, position, radius=5)
    
    # Remove event from the map
    def remove_event(self, event, position):
        x = position[0]
        y = position[1]
        self.case_details[x, y]["events"].remove(event)
    
    # Commend agent to perceive the environment
    def activate_perceive(self, position, time):
        
        x = position[0]
        y = position[1]
        for i in range(x-5, x+6):
            if 0 <= i < self.height:
                for j in range(y-5, y+6):
                    if 0 <= j < self.width:
                        for agent in self.case_details[i,j]["agents"]:
                            agent.perceive(time,self.nearby(agent.position))
    
    # Add event to the map
    def add_event(self, event, position, time):
        
        x = position[0]
        y = position[1]
        self.case_details[x, y]["events"].add(event)
        self.activate_perceive(position, time)

class Environment:
    def __init__(self, start_env_time=time.time(), min_equivalent_seconds=1):
        self.map = Map()
        self.start_env_time = start_env_time
        self.min_equivalent_seconds = min_equivalent_seconds
        self.queue_of_configurations = []
        self.num = 0
        
    def get_time(self):
        return time.time() - self.start_env_time
    
    def get_min_equivalent_seconds(self):
        return self.min_equivalent_seconds
    
    def get_duration_equivalent(self, start, end):
        return get_duration(start, end) * self.min_equivalent_seconds
    
    def add_configuration_to_the_queue(self, configuration):
        self.queue_of_configurations.append(configuration)
    
    def pop_configuration_from_the_queue(self):
        return self.queue_of_configurations.pop(0)
from back_end.agent.plan import create_initial_plan, create_sub_plan
from back_end.agent.functions import get_info, add_event_to_sensory_memory
from back_end.agent.execute import execute_sub_task 
from back_end.short_term_memory.st_memory import Short_Memory
from back_end.long_term_memory.episodic_memory.epis_mem import EpisodicMemoryGraph
from back_end.long_term_memory.emotion import Emotion
from back_end.long_term_memory.personality import Personality

class Agent:
    def __init__(self, id, current_event = None, position=(4,4)):
        self.id = id
        self.file_path = f'back_end/memory/{id}/'
        self.name = self.get_info()['name']
        self.position = position
        self.sensory_memory = []
        self.st_memory = Short_Memory(self.id)
        self.lt_memory = EpisodicMemoryGraph()
        self.emotion = Emotion(0,0,0,0,0,0,0,0,0,0) #to be introduced in the init later
        self.personality = Personality(0, 0, 0, 0, 0) #to be introduced in the init later
        self.seen = set()

        # The current event the agent is executing
        self.current_event = current_event

    # Get identity info from memory to create initial plan
    def get_info(self):
        return get_info(self)
    
    # Create initial plan and save it in memory
    def create_initial_plan(self):
        return create_initial_plan(self.get_info(), self.file_path)
    
    # Create sub plan for task_i and save it in memory
    def create_sub_plan(self, i, localisations):
        return create_sub_plan(i, self.file_path, localisations)
    
    # add event to the sensory memory
    def add_event_to_sensory_memory(self, event, pos):
        add_event_to_sensory_memory(self, event, pos)
    
    # Clear the seen set
    def clear_seen(self):
        self.seen = set()

    # Clear the sensory memory
    def clear_memory(self):
        self.sensory_memory = []

    # Execute sub task task between start and end at localisation in environment
    def execute_sub_task(self, start, end, localisation, task, environment):
        execute_sub_task(self, start, end, localisation, task, environment)
    
    # Get information about the environment and put it on the long term memory
    def perceive(self, time, events):
        
        unique_events = []
        if events is not None:
            
            for event in events:
                if event[0] not in self.seen:
                    unique_events.append(event[0])
                    self.seen.add(event[0])
            keep=self.st_memory.filter(self, unique_events,time)
            if keep is not None:
                for event in keep:
                    self.emotion.update_emotion(event)
                    self.lt_memory.add_connected_node(event)
            else:
                print("keep is None")
        else:
            pass
                
    # Squeeze the relevant information from the information perceived
    def retreive(self):
        pass
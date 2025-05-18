DEFAULT_STATE = 0
TEXT_STATE = 1
IMAGE_STATE = 2

class FSM:
    def __init__(self):
        self.states = {}

    def get_state(self, uid):
        if uid not in self.states:
            self.states[uid] = DEFAULT_STATE
        return self.states[uid]
    
    def set_state(self, uid, state):
        self.states[uid] = state
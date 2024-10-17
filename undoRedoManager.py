class UndoRedoManager:
    def __init__(self, limit=300):
        self.nextStates = []
        self.previousStates = []
        self.limit = limit

    def _trim_list(self, state_list):
        if len(state_list) > self.limit:
            state_list.pop(0)

    def undo(self):
        state = self.previousStates.pop() if self.previousStates else None
        return state[0], state[1], state[2]

    def redo(self):
        state = self.nextStates.pop() if self.nextStates else None
        return state[0], state[1], state[2]

    def get_next_states(self):
        return self.nextStates

    def get_previous_states(self):
        return self.previousStates

    def add_previous_states(self, qImage, brightnessValue, widthValue):
        self.previousStates.append([qImage, brightnessValue, widthValue])
        self._trim_list(self.previousStates)
        print("Length previousImages: " + str(len(self.previousStates)))

    def add_next_states(self, qImage, brightnessValue, widthValue):
        self.nextStates.append([qImage, brightnessValue, widthValue])
        self._trim_list(self.nextStates)
        print("Length nextImages: " + str(len(self.nextStates)))

    def reset_next_images(self):
        self.nextStates = []

    def reset_previous_states(self):
        self.previousStates = []

class Node:

    def __init__(self, message):
        self.message = message
        self.responses = {}

    def add_response(self, input, new_node):
        self.responses[input] = new_node

    def get_message(self):
        return self.message

    def get_next_node(self, input):
        if (self.responses):
            return self.responses[input]
        else:
            return None

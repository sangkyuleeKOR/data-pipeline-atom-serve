

class DataTransmitter:

    def __init__(self):
        self.components = {}

    def observe(self, _type, component):
        if not _type in self.components:
            self.components[_type] = []
        self.components[_type].append(component)

    def push(self, event):
        if event['type'] in self.components:
            for component in self.components[event['type']]:
                component.add_data(event['meta'], event['data'])


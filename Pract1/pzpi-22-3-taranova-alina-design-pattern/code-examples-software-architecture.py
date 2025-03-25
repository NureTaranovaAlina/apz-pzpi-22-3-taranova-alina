import copy

class Car:
    def __init__(self, model, color):
        self.model = model
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

car1 = Car("BMW", "black")
car2 = car1.clone()
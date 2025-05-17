import random


class Connection:
    def __init__(self, in_, out, weight, number, enable=True):
        self.in_ = in_
        self.out = out
        self.weight = weight
        self.enable = enable
        self.innovation_number = number
        self.weight_min = -1
        self.weight_max = 1

    '''
    change the weight by perturb or change the weight
    '''
    def mutate_weight(self, perturb):
        if random.random() < perturb:
            self.weight += random.uniform(-0.1, 0.1)
        else:
            self.weight = random.uniform(-0.5, 0.5)

        if self.weight > self.weight_max:
            self.weight = self.weight_max
        elif self.weight < self.weight_min:
            self.weight = self.weight_min


    '''
    turn the connection on or off.
    '''
    def toggle_enable(self):
        self.enable = not self.enable

    '''
    check if the connection is on or off
    '''
    def get_state(self):
        return self.enable

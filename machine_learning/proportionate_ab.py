import random

class ProportionateAB(object):
    def __init__(self, choices):
        self.choices = choices
        self.num_choices = len(choices)
        self.As = [0] * self.num_choices
        self.Bs = [0] * self.num_choices
        self.chosen_index = None

    def choose(self):
	best_sample_value = 0.0
        for i in xrange(self.num_choices):
            sample_value = random.betavariate(self.As[i]+1, self.Bs[i]+1)
            if sample_value > best_sample_value:
                best_sample_value = sample_value
                self.chosen_index = i

        return self.choices[self.chosen_index]
        
    def update(self, success):
        if success:
            self.As[self.chosen_index] += 1
        else:
            self.Bs[self.chosen_index] += 1

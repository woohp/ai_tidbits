import random

class EpsilonGreedy(object):
    def __init__(self, choices, epsilon):
        self.choices = choices
        self.num_choices = len(choices)
        self.epsilon = epsilon
        self.tries = [0] * self.num_choices
        self.successes = [0.0] * self.num_choices
        self.chosen_index = None

    def choose(self):
        if random.random() < self.epsilon:
            self.chosen_index = random.randint(0, self.num_choices-1)
        else:
            self.chosen_index = 0
            best_ratio = self.successes[0] / self.tries[0]
            for i in xrange(1, len(self.choices)):
                ratio = self.successes[i] / self.tries[i]
                if ratio > best_ratio:
                    best_ratio = ratio
                    self.chosen_index = i

        self.tries[self.chosen_index] += 1
        return self.choices[self.chosen_index]

    def update(self, success):
        self.successes[self.chosen_index] += int(success)

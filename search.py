import numpy as np
from time import time


class Search:

    def __init__(self, elements):
        """
        Find the index if the random variable with the highest
        average value in the smallest number of steps.

        :param elements: elements[i]() should return
            evaluation of the i-th element
        """
        self.elements = elements
        self.n_elements = len(elements)
        self.values = [[] for _ in range(len(elements))]
        self.averages = np.zeros(len(elements))
        self.visits = np.zeros(len(self), dtype=int)
        self.total_visits = 0
        self.scores = np.zeros(len(self))

    def __len__(self):
        return self.n_elements

    def _get_best_index_and_value(self):
        """get index and value of current best element"""
        index = np.argmax(self.scores)
        value = self.averages[index]
        return index, value

    def _compute_scores(self, minimize=False):
        """update scores based on current values and visits"""

        # compute min, max, and average
        values = np.array([self.averages[i] for i in range(len(self.elements))])
        _min = np.min(values)
        _max = np.max(values)
        _avg = np.average(values)

        # substitute not visited elements with average value
        self.scores = self.averages + (self.visits == 0) * _avg

        # normalize
        self.scores -= np.min(self.scores)
        _max = np.max(self.scores)
        if _max:
            self.scores /= _max
        if minimize:
            self.scores = 1 - self.scores

    def _compute_priorities(self, c=2.):
        """return list of priorities given by the magic formula"""
        return self.scores + c * np.sqrt(np.log(self.total_visits / self.visits))

    def _get_high_priority_index(self, c=2.):
        """return index of element with the highest priority"""
        return np.argmax(self._compute_priorities(c))

    def _update_values(self, index, new_value, metric=np.average):
        """append new value to the list of values of the element with the given index"""
        self.values[index].append(new_value)
        self.averages[index] = metric(self.values[index])

    def _visit(self, index, metric=np.average):
        """get new value from high-priority element, then update visits and scores"""

        # sample the element
        new_value = self.elements[index]()

        # update
        self._update_values(index, new_value, metric=metric)
        self.visits[index] += 1
        self.total_visits += 1

    def get_most_visited_index(self):
        """return index and number of visits for the most visited element"""
        index = np.argmax(self.visits)
        return index, self.visits[index]

    def get_info(self) -> dict:
        """return dictionary with the relevant info"""
        best_index, best_value = self._get_best_index_and_value()
        most_visited_index, most_visits = self.get_most_visited_index()

        return {'iteration': self.total_visits,
                'best_index': best_index,
                'best_value': best_value,
                'most_visited_index': most_visited_index,
                'most_visits': most_visits,
                'visits': self.visits,
                }

    def run_search_iter(self, n_iter=None, minimize=False, time_limit=None, c=2., metric=np.average, min_visits=1):
        """run search
        Iterating over an instance of this method yields a dictionary
        with the relevant info. The search stops after n_iter iterations.
        First visit all elements one by one, then visit the most promising ones.
        """
        t0 = time()
        n_stop = 0
        if n_iter is not None:
            n_stop = self.total_visits + n_iter

        while True:
            if n_iter is not None:
                if self.total_visits >= n_stop:
                    break
            if time_limit and time() - t0 > time_limit:
                break

            if self.total_visits < len(self.elements) * min_visits:
                new_index = self.total_visits % len(self.elements)
            else:
                self._compute_scores(minimize)
                new_index = self._get_high_priority_index(c)

            self._visit(new_index, metric=metric)
            self._compute_scores(minimize)
            yield self.get_info()

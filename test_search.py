import numpy as np
import matplotlib.pyplot as plt
from time import time
from search import Search


def test_plot(n_elements=20, n_visits_per_element=15, noise=0.3, c=1., random_state=42):
    np.random.seed(random_state)
    t = time()

    # to save evaluations for the plot
    values = [[] for _ in range(n_elements)]

    averages = [i / (n_elements - 1) for i in range(n_elements)]
    deviations = (np.random.rand(n_elements) + 0.5) * noise

    # define elements to explore
    def element(index):
        """evaluate a fictitious element of a certain index"""

        def wrap():
            value = averages[index] + deviations[index] * np.random.normal()
            values[index].append(value)
            return value

        return wrap

    elements = [element(i) for i in range(n_elements)]

    # run search
    search = Search(elements)
    count = np.zeros(n_elements, dtype=int)
    first_count = np.zeros(n_elements, dtype=int)
    search_iter = search.run_search_iter(n_iter=n_elements * n_visits_per_element, c=c, metric=np.average)
    best_index = []
    most_visited_index = []

    # take track of visits (*optional)
    dct = None
    for i, dct in enumerate(search_iter):
        count[dct["best_index"]] += 1
        if i <= n_elements:
            first_count[dct["best_index"]] += 1
        best_index.append(dct["best_index"])
        most_visited_index.append(dct["most_visited_index"])

    visits = dct['visits']

    t = time() - t
    print(f'\ntime = {t:.2f} s')

    # plot (*optional)
    fig, ax = plt.subplots(nrows=2, ncols=2)
    plt.suptitle(f'Results of the search with {n_elements} random variables '
                 f'after {dct["iteration"]} iterations')

    plt.sca(ax[0, 0])
    plt.title(' #times voted as best', loc='left', pad=-14, y=1.)
    plt.bar(list(range(1, 1 + n_elements)), count, width=1)
    plt.bar(list(range(1, 1 + n_elements)), first_count, width=1, color='k', alpha=0.3)
    plt.xticks([])
    plt.ylabel('count')
    plt.xlim(0, n_elements + 1)

    plt.sca(ax[0, 1])
    plt.title(' #times visited', loc='left', pad=-14, y=1.)
    plt.bar(list(range(1, 1 + n_elements)), visits, width=1, color='r')
    plt.bar(list(range(1, 1 + n_elements)), np.ones(n_elements), width=1, color='k', alpha=0.3)


    plt.xticks([])
    plt.ylabel('count')
    plt.xlim(0, n_elements + 1)

    plt.sca(ax[1, 0])
    plt.title(' values', loc='left', pad=-14, y=1.)
    for i in range(n_elements):
        plt.scatter(np.ones(len(values[i])) * i + 1, values[i], color='k', alpha=.2, edgecolors="none", s=50)
    plt.xlim(0, n_elements + 1)
    plt.plot([1, n_elements], [0, 1], 'k--', alpha=0.5, label='true mean')
    plt.text(x=1, y=0.05, s=f'true mean', alpha=0.8, fontdict={'size': 8, 'rotation': 14})
    plt.xticks(list(range(1, 1 + n_elements)))
    plt.xlabel('element index')
    plt.ylabel('value')
    plt.xlim(0, n_elements + 1)

    plt.sca(ax[1, 1])
    plt.title(' best index', loc='left', pad=-14, y=1.)
    plt.plot([0, n_elements], [n_elements, n_elements], 'k--', alpha=0.2)
    plt.text(x=1, y=n_elements+2, s=f'{n_elements} visits', alpha=0.8, fontdict={'size': 8})
    _y = list(range(len(best_index)))
    plt.scatter(best_index, _y, c='orange')
    plt.scatter(best_index[:n_elements], _y[:n_elements], c='k', alpha=0.13, edgecolors="none", s=50)
    plt.xticks(list(range(n_elements)), [str(i) for i in range(1, 1 + n_elements)])
    plt.xlabel('element index')
    plt.ylabel('iteration')
    plt.xlim(-1, n_elements)

    # decrease the space between subplots
    plt.subplots_adjust(hspace=0., wspace=0.18)

    plt.show()


if __name__ == '__main__':
    test_plot()

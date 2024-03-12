import numpy as np
from search import Search


def example_1(n_elements=1000, c=2., time_limit=3., noise=0.5):
    np.random.seed(42)

    # define your program
    def program(parameter):
        def wrap():
            return parameter / (n_elements - 1) + np.random.normal() * noise

        return wrap

    parameters = list(range(n_elements))
    elements = [program(par) for par in parameters]

    # run search
    search = Search(elements)
    search_iter = search.run_search_iter(time_limit=time_limit, c=c)
    dct = None
    for dct in search_iter:
        i = dct['iteration']
        if i % 100 == 0:
            print(f'\ri={i}  best_index={dct["best_index"]}  best_val={dct["best_value"]:.2f}', end=' ')

    # print results
    print('\n\n')
    print(f'iterations = {dct["iteration"]}')
    print()
    print(f'max_visits = {np.max(dct["visits"])}')
    print(f'avg_visits = {np.average(dct["visits"]):.1f}')
    print(f'min_visits = {np.min(dct["visits"])}')
    print()
    print(f'n_elements = {n_elements}')
    print(f'best_param = {dct["best_index"]}')
    print(f'best_value = {dct["best_value"]:.3f}')


def example_2(n_elements=1000, noise=1.):
    """Example of a search with a large number of normal random variables"""
    np.random.seed(42)

    # define your program
    def program(parameter):
        k = 1 / (n_elements - 1)

        def wrap():
            return parameter * k + np.random.normal() * noise

        return wrap

    parameters = list(range(n_elements))
    elements = [program(par) for par in parameters]

    # run search
    search = Search(elements)
    search_iter = search.run_search_iter()
    for dct in search_iter:
        i = dct['iteration']
        if i % 100 == 0:
            print(f'\ri={i}  best_index={dct["best_index"]}  best_val={dct["best_value"]:.2f}', end=' ')


if __name__ == '__main__':
    example_1()
    # example_2()

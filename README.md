# SearchHeuristic
optimization for finding optimal random variables

The Search class searches for the best variable of a list of random variables. 
Each random variable is sampled by calling it.
The goal is to identify which random variables provided have a reasonably high expected value with a reasonably low number of samples.
By calling the run_search_iter method you can get the status of the search after each iteration.

```
elements = [callable_1, ..., callable_n]
search = Search(elements)
search_iter = search.run_search_iter(time_limit=time_limit, c=c)
for dct in search_iter:
  print(dct)
```

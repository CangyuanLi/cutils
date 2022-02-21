Some personal Python utilities. Only uses standard library.

# Gotchas

## Dictionaries

What is the difference between

```{python}
dict1 = dict(zip(["a", "b", "c"], [[]] * 3))
```
and 

```{python}
dict2 = {key:[] for key in ["a", "b", "c"]}
```
When you print them, both return

```{python}
{'a': [], 'b': [], 'c': []}
```
But try, for example, 

```{python}
dict1["a"].append(1)
print(dict1)
dict2["a"].append(1)
print(dict2)
```

Surprisingly, you get

```{python}
dict1 = {'a': [1], 'b': [1], 'c': [1]}
dict2 = {'a': [1], 'b': [], 'c': []}
```
What happened here? The empty lists in dict1 are actually the same list, so when you change one, you change all of them. You can run into the same trap if you initialize a dictionary with

```{python}
dict.fromkeys(["a", "b", "c"], [])
```

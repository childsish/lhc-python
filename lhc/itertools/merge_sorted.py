from typing import Any, Iterator, List


def merge_sorted(*iterators: List[Any]) -> Iterator[List[Any]]:
    tops = [next(iterator, None) for iterator in iterators]
    smallest_indices = get_smallest_indices(tops)
    while len(smallest_indices) > 0:
        yield get_at_indices(tops, smallest_indices, iterators)
        smallest_indices = get_smallest_indices(tops)


def get_smallest_indices(tops):
    smallest = []
    for i, item in enumerate(tops):
        if item is None:
            continue

        if len(smallest) == 0 or item < tops[smallest[0]]:
            smallest = [i]
        elif item == tops[smallest[0]]:
            smallest.append(i)
    return smallest


def get_at_indices(tops, indices: List[int], iterators: List[Iterator]) -> List[Any]:
    result = [tops[index] for index in indices]
    for index in indices:
        tops[index] = next(iterators[index], None)
    return result

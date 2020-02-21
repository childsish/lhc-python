from typing import Any, Iterator, List, Tuple


def merge_sorted(*iterators: Iterator[Any]) -> Iterator[List[List[Any]]]:
    tops = [next(iterator, None) for iterator in iterators]
    smallest_indices = get_smallest_indices(tops)
    while len(smallest_indices) > 0:
        yield get_at_indices(tops, smallest_indices, iterators)
        smallest_indices = get_smallest_indices(tops)


def get_smallest_indices(tops) -> List[int]:
    smallest = []
    for i, item in enumerate(tops):
        if item is None:
            continue

        if len(smallest) == 0 or item < tops[smallest[0]]:
            smallest = [i]
        elif item == tops[smallest[0]]:
            smallest.append(i)
    return smallest


def get_at_indices(tops, indices: List[int], iterators: Tuple[Iterator[Any]]) -> List[List[Any]]:
    result = []
    for index in indices:
        result.append([tops[index]])
        tops[index] = next(iterators[index], None)
        while tops[index] == result[-1][0]:
            result[-1].append(tops[index])
            tops[index] = next(iterators[index], None)
    return result

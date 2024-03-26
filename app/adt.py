# Author: Marek Jankech

class CircularList:
    def __init__(self, lst) -> None:
        if not lst:
            raise ValueError
        self._lst = lst
        self._index = None
        self._max_index = len(lst) - 1

    def next(self):
        if self._index is None or self._index == self._max_index:
            self._index = 0
        else:
            self._index += 1        
        return self._lst[self._index]

    def prev(self):
        if self._index is None or self._index == 0:
            self._index = self._max_index
        else:
            self._index -= 1
        return self._lst[self._index]
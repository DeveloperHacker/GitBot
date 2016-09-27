from copy import copy, deepcopy


class Shell:
    @property
    def adjectives(self):
        return self._adjectives

    @property
    def functions(self):
        return self._functions

    def __init__(self, adjectives: list, functions: list):
        self._adjectives = adjectives
        self._functions = functions

    def difference(self, adjectives: list) -> list:
        copy_list = deepcopy(self._adjectives)
        result = []
        for element in adjectives:
            if element in copy_list:
                copy_list.remove(element)
            else:
                result.append(element)
        return result

    def distance(self, adjectives: list):
        return abs(len(adjectives) - len(self._adjectives))

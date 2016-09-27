def __static__() -> (dict, dict, dict, set):
    _units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"
    ]
    _ordinal = {
        0: "zero", 1: "first", 2: "second", 3: "third", 5: "fifth", 8: "eighth", 9: "ninth", 12: "twelfth"
    }
    _tens = [
        "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
    ]
    _scales = [
        "hundred", "thousand", "million", "billion", "trillion"
    ]
    _units = {word: i for i, word in enumerate(_units)}
    _tens = {word: (i + 2) * 10 for i, word in enumerate(_tens)}
    _scales = {word: 10 ** (i * 3 or 2) for i, word in enumerate(_scales)}
    _units.update({(_ordinal[value] if value in _ordinal else word + "th"): value for word, value in _units.items()})
    _tens.update({word + "th": value for word, value in _tens.items()})
    _scales.update({word + "th": value for word, value in _scales.items()})
    return _units, _tens, _scales, set(_units.keys()) | set(_tens.keys())


class Number:
    _units, _tens, _scales, _numbers = __static__()

    class Token:
        def __init__(self, word: str):
            word = word.lower()
            self.plural = word[-1] == 's'
            if len(word) > 1 and word[-1] == 's':
                word = word[:-1]
            elif len(word) > 2 and word[-2:] == 'st' and word[:-2].isnumeric():
                word = word[:-2]
            self.word = word
            if word in Number._units:
                self.value = Number._units[word]
                self.power = 0
            elif word in Number._tens:
                self.value = Number._tens[word]
                self.power = 1
            elif word in Number._scales:
                self.value = Number._scales[word]
                self.power = 3
            elif word.isnumeric():
                self.value = int(word)
                self.power = 2
            else:
                self.value = None
                self.power = None

    @property
    def value(self) -> int:
        return self._value

    @property
    def words(self) -> list:
        return self._words

    def __init__(self, words: list):
        self._value = Number.integer(words)
        self._words = words

    def __int__(self) -> int:
        return self._value

    def __str__(self) -> str:
        return ' '.join(self._words)

    def __getitem__(self, index):
        return self._words[index]

    @staticmethod
    def collapse(words: list) -> list:
        result = []
        number = []
        for word in words:
            if Number.isnumber(word):
                number.append(word)
            elif len(number) != 0:
                result.append(Number(number))
                result.append(word)
                number = []
            else:
                result.append(word)
        if len(number) != 0: result.append(Number(number))
        return result

    # ToDo:
    @staticmethod
    def words(integer: int) -> str:
        pass

    @staticmethod
    def integer(words: list) -> int:
        result = []
        current = None
        prev_power = float("inf")
        for word in words:
            token = Number.Token(word)
            if prev_power == token.power and not token.plural or token.power == 2:
                result.append(str(current if current else 0))
            if token.power in {0, 1}:
                if prev_power > token.power:
                    current = token.value + (current if current else 0)
                elif token.plural:
                    current *= token.value
                else:
                    current = token.value
            elif token.power == 2:
                current = int(word)
            elif token.power == 3:
                current = Number._scales[word]
            prev_power = token.power
        result.append(str(current))
        result = "".join(result)
        return 0 if result == "" else int(result)

    @staticmethod
    def isnumber(words) -> bool:
        if isinstance(words, int): return True
        elif isinstance(words, str): words = words.split()
        else: return False
        for word in words:
            token = Number.Token(word)
            if token.power is None: return False
        return True


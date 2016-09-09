import os

if os.getenv("SRC_MAIN_NLP_INIT_NUMBER") == "false":
    os.environ["SRC_MAIN_NLP_INIT_NUMBER"] = "true"

    def __static__() -> (dict, dict, dict, set):
        _units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
            "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"
        ]
        _ordinal = [
            "zero", "first", "second", "third"
        ]
        _tens = [
            "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
        ]
        _scales = [
            "hundred", "thousand", "million", "billion", "trillion"
        ]
        _units = {word: i for i, word in enumerate(_units)}
        _tens = {word: (i + 2) * 10 for i, word in enumerate(_tens)}
        _scales = {word: 10 ** (i * 3 or 2) for i, word in enumerate(_scales)}
        _units.update(
            {(_ordinal[value] if value < len(_ordinal) else word + "th"): value for word, value in _units.items()})
        _tens.update({word + "th": value for word, value in _tens.items()})
        _scales.update({word + "th": value for word, value in _scales.items()})
        return _units, _tens, _scales, set(_units.keys()) | set(_tens.keys())


    class Number:
        _units, _tens, _scales, _numbers = __static__()

        def __init__(self, words: list):
            self._value = Number.number(words)
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
                if Number.is_number([word]):
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
        def number(words: list) -> int:
            result = []
            current = None
            prev_power = float("inf")
            for word in words:
                word = word.lower()
                plural = word[-1] == 's'
                if len(word) > 1 and word[-1] == 's': word = word[:-1]
                elif len(word) > 2 and word[-2:] == 'st' and word[:-2].isnumeric(): word = word[:-2]
                if word in Number._units or word in Number._tens:
                    for power, nums in [(0, Number._units), (1, Number._tens)]:
                        if word in nums:
                            if prev_power > power:
                                current = nums[word] + (current if current else 0)
                            elif plural:
                                current *= nums[word]
                            else:
                                result.append(str(current))
                                current = nums[word]
                            prev_power = power
                elif word in Number._scales:
                    if prev_power < 2 or plural:
                        current *= Number._scales[word]
                    else:
                        result.append(str(current))
                        current = Number._scales[word]
                    prev_power = 2
                elif word.isnumeric():
                    result.append(str(current if current else 0))
                    current = int(word)
                    prev_power = 1
            result.append(str(current))
            result = ''.join(result)
            return 0 if result == '' else int(result)

        @staticmethod
        def is_number(words) -> bool:
            for word in words:
                word.lower()
                if len(word) > 1 and word[-1] == 's': word = word[:-1]
                elif len(word) > 2 and word[-2:] == 'st' and word[:-2].isnumeric(): word = word[:-2]
                if not(word in Number._units
                       or word in Number._tens
                       or word in Number._scales
                       or word.isnumeric()):
                    return False
            return True

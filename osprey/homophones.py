# https://github.com/pimentel/homophones

from pathlib import Path

HOMOPHONES = {}

HOMOPHONES_FILENAME = "homophones.csv"
HOMOPHONES_FILEPATH = Path(__file__).parent / HOMOPHONES_FILENAME

for line in HOMOPHONES_FILEPATH.read_text().splitlines():
    words = sorted(line.split(","))
    for word in words:
        words_copy = words.copy()
        words_copy.remove(word)
        HOMOPHONES[word.lower()] = words_copy

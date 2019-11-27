# https://github.com/pimentel/homophones

from pathlib import Path

homophones_filename = "homophones.csv"
homophones_filepath = Path(__file__).parent / homophones_filename

HOMOPHONES = {}

for line in homophones_filepath.read_text().splitlines():
    words = sorted(line.split(","))
    for word in words:
        HOMOPHONES[word.lower()] = words

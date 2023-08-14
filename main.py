import json
import random
import os

JSON_FILEPATH = os.path.join("data", "dico.json")
with open(JSON_FILEPATH, "r") as f:
    data = json.load(f)


def find_word(lettre):
    for keys in data:
        value = random.choice(list(data[keys][lettre]))
        print(keys, ":", value)


find_word("a")


# get_word("A")

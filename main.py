import json
from random import choice

with open("dico.json", "r") as read_file:
    data = json.load(read_file)


# for key in data.keys():
test = data["animaux"].keys()
print(test.values())


def get_word(letter):
    pass


# get_word("A")

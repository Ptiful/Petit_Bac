import requests
import pandas

root_url = "https://liste-mots.com/dico-du-petit-bac/"
x = requests.get(root_url).text
print(x)

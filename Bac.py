# Import necessary modules and libraries
import re
import json
from functools import partial
import requests
from bs4 import BeautifulSoup
from tqdm.contrib.concurrent import thread_map


# Function to retrieve URLs from a given URL
def get_urls(url, session=None):
    req = session.get(url)  # Send a GET request to the URL
    soup = BeautifulSoup(req.text, "lxml")  # Parse the response using BeautifulSoup
    return (
        link["href"] for link in soup.select("a[href^='https://dico-petitbac.com']")
    )


# Regular expression pattern to match letter categories
LETTER_RE = re.compile(r"^.*-[a-z]$")


# Function to retrieve category, letter, and sub-URLs from a base URL
def get_categories_letters_urls(base_url, session=None):
    for url in get_urls(
        base_url, session
    ):  # Iterate over URLs obtained from get_urls()
        for sub_url in get_urls(
            url, session
        ):  # Iterate over URLs obtained from the first iteration
            split = sub_url.split("/")
            penultimate_part = split[-2]
            if LETTER_RE.match(
                penultimate_part
            ):  # Check if penultimate part of the URL matches the pattern
                letter = penultimate_part[-1]
                category = split[-3]
                yield category, letter, sub_url  # Yield the category, letter, and sub-URL


# Function to retrieve words from a given category, letter, and sub-URL
def get_words(args, session=None):
    category, letter, sub_url = args
    req = session.get(sub_url)  # Send a GET request to the sub-URL
    soup = BeautifulSoup(req.text, "lxml")  # Parse the response using BeautifulSoup
    return (
        category,
        letter,
        [li.text for li in soup.select("li")],
    )  # Return category, letter, and list of words


# Function to retrieve the dictionary of data from the website
def get_dico():
    base_url = "https://dico-petitbac.com/"
    dico = {}  # Initialize an empty dictionary
    with requests.Session() as session:  # Create a requests session
        categories_letters_urls = list(
            get_categories_letters_urls(base_url, session)
        )  # Get category, letter, and sub-URLs
        for category, letter, words in thread_map(
            partial(get_words, session=session), categories_letters_urls
        ):
            # Concurrently execute get_words() for each tuple of category, letter, and sub-URL
            dico.setdefault(category, {}).setdefault(letter, []).extend(
                words
            )  # Populate the dictionary with words
    return dico


# Function to save the dictionary to a JSON file
def save_dicto(dico):
    with open("dico.json", "w") as f:
        json.dump(dico, f)


# Get the dictionary of data from the website
dico = get_dico()
# Save the dictionary to a JSON file
save_dicto(dico)

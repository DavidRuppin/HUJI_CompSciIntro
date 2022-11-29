#################################################################
# FILE : moogle_logic.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex6 2022-2023
#################################################################
import pickle
import urllib.parse
from collections import defaultdict

from pprint import pprint
import bs4
import requests


# HELPER FUNCTIONS #
def join_urls(base_url, relative_url):
    """Mounts a relative url on a base url.
    For example: join_urls('www.WHUPF.com/index.html', 'ryans_secret.html') == 'www.WHUPF.com/ryans_secret.html'
    """
    return urllib.parse.urljoin(base_url, relative_url).strip()


def get_page_html(url):
    """Gets the HTML of a URL"""
    response = requests.get(url)
    return response.text


def get_all_hrefs(html) -> dict:
    """Finds all the hrefs in a given url and returns a dictionary in the following format: links[href] = href.count"""
    soup = bs4.BeautifulSoup(html, 'html.parser')

    links = {}  # link: number of times it appeared in the page

    for p in soup.find_all('p'):
        for link in p.find_all('a'):
            # If the link is in the dict already, increase the counter. Otherwise, add it and start counting
            links[link.get('href')] = links.get(link.get('href'), 0) + 1

    return links


def get_all_paragraphs(html) -> list:
    """Finds all the paragraphs in a given url and returns a list containing their content"""
    soup = bs4.BeautifulSoup(html, 'html.parser')

    paragraphs = []

    for p in soup.find_all('p'):
        paragraphs.append(p.text)

    return paragraphs


def get_all_words_from_paragraphs(paragraphs: list[str]) -> list:
    words = []
    for paragraph in paragraphs:
        for word in paragraph.split():
            if len(word.strip()) > 0:
                words.append(word.strip())

    return words


def read_index_file(path):
    """Returns a list of relative links in a file at a given path. Each line is considered a link.
    The lines are stripped of whitespaces"""
    links = []
    with open(path, 'r') as fp:
        for line in fp.readlines():
            links.append(line.strip())

    return links


def filter_dictionary_items(dictionary: dict, items_to_keep: list) -> dict:
    """Iterates over the dictionary and creates a new dictionary strictly with the keys from @items_to_keep"""
    new_dict = {}
    for key in dictionary.keys():
        if key in items_to_keep:
            new_dict[key] = dictionary[key]

    return new_dict


def object_to_pickle(obj, pickle_save_path):
    """Saves an object to a pickle file at @pickle_save_path"""
    with open(pickle_save_path, 'wb') as fp:
        pickle.dump(obj, fp)


def object_from_pickle(pickle_path):
    """Loads the pickle from pickle_path. Assuming that the given path is a valid pickle"""
    with open(pickle_path, 'rb') as fp:
        return pickle.load(fp)


def get_total_num_links_from_page(page_href_dict: dict) -> int:
    """Returns the number of links from a {link:link_count} dictionary. Assuming all the values are integers"""
    return sum(page_href_dict.values())


# END OF HELPER FUNCTIONS #

def crawl(base_url: str, index_file: str, out_file: str):
    traffic_dict = {}
    index_file_links = read_index_file(index_file)
    for link in index_file_links:
        full_url = join_urls(base_url, link)
        html = get_page_html(full_url)
        href_dict = get_all_hrefs(html)
        href_dict = filter_dictionary_items(href_dict, index_file_links)
        traffic_dict[link] = href_dict

    object_to_pickle(traffic_dict, out_file)


def page_rank(iterations: int, dict_file: str, out_file: str):
    reference_dict = object_from_pickle(dict_file)

    # Initializing the rank_dict to default to 1
    rank_dict = defaultdict(lambda: 1)
    for iteration in range(iterations):
        iter_dict = defaultdict(int)
        for page in reference_dict:
            for link in reference_dict[page]:
                iter_dict[link] += \
                    rank_dict[page] * (reference_dict[page][link] / get_total_num_links_from_page(reference_dict[page]))
        rank_dict = iter_dict

    object_to_pickle(rank_dict, out_file)


def words_dict(base_url: str, index_file: str, out_file: str):
    word_dict = defaultdict(dict)

    page_links = read_index_file(index_file)
    for page in page_links:
        full_url = join_urls(base_url, page)
        html = get_page_html(full_url)
        for word in get_all_words_from_paragraphs(get_all_paragraphs(html)):
            word_dict[word][page] = word_dict[word].get(page, 0) + 1

    object_to_pickle(word_dict, out_file)

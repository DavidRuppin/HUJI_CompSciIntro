#################################################################
# FILE : moogle_logic.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex6 2022-2023
#################################################################
import pickle
import urllib.parse

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


def get_all_hrefs(url):
    """Finds all the hrefs in a given url and returns a dictionary in the following format: links[href] = href.count"""
    html = get_page_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')

    links = {}  # link: number of times it appeared in the page

    for p in soup.find_all('p'):
        for link in p.find_all('a'):
            # If the link is in the dict already, increase the counter. Otherwise, add it and start counting
            links[link.get('href')] = links.get(link.get('href'), 0) + 1

    return links


def dict_to_pickle(dictionary, pickle_save_path):
    """Saves a dictionary to a pickle file at @pickle_save_path"""
    with open(pickle_save_path, 'wb') as fp:
        pickle.dump(dictionary.f)


def read_index_file(path):
    """Returns a list of relative links in a file at a given path. Each line is considered a link"""
    links = []
    with open(path, 'r') as fp:
        for line in fp.readlines():
            links.append(line.strip())

    return links


# END OF HELPER FUNCTIONS #

def crawl(base_url: str, index_file: str, out_file: str):
    print(base_url, index_file, out_file)
    traffic_dict = {}
    for link in read_index_file(index_file):
        full_url = join_urls(base_url, link)
        hrefs = get_all_hrefs(full_url)
        traffic_dict[link] = hrefs

    pprint(traffic_dict)
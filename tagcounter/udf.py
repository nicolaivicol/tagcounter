import logging
import requests
import json
import yaml
import tkinter as tk
from bs4 import BeautifulSoup
from tagcounter.db import write_to_db, view_from_db
from tagcounter.gui import MainWindowGUI


def get_html_txt(x_url: str):
    """Get the html of the page of a given url and return it as a string."""
    txt = ''
    try:
        r = requests.get(x_url, timeout=5)
        if r.status_code != 200:
            logging.warning("Status code not OK: " + str(r.status_code))
        txt = r.text
    except requests.exceptions.ConnectionError as err_ce:
        logging.error("Connection error: " + str(err_ce))
    except requests.exceptions.Timeout as err_timeout:
        logging.error("Timeout error: " + str(err_timeout))
    except Exception as err:
        logging.error('Error occurred: ' + str(err))
    finally:
        return txt


def html_tags(html_txt: str):
    """Count html tags in a html text and return a dictionary with html tags as keys and counts as values."""
    s = BeautifulSoup(html_txt, features='html.parser')
    tags = []
    for child in s.recursiveChildGenerator():
        if child.name:
            tags.append(child.name)
    return tags

def word_frequency(words: list):
    """Counts word frequency from a list of words and returns a desc ordered dictionary with words as keys and counts
    as values."""
    words_count = {}
    for w in words:
        if (w in words_count):
            words_count[w] += 1
        else:
            words_count[w] = 1
    words_count = dict(sorted(words_count.items(), key=lambda kv: kv[1], reverse=True))
    return words_count


def read_sites_synonyms_from_yaml(file_path_yaml: str):
    """Read yaml with site synonyms"""
    dict_sites = {}
    with open(file_path_yaml, 'r') as stream:
        try:
            dict_sites = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
    return dict_sites


def select_synonym_from_dict(site_name: str, dict_sites: dict):
    try:
        site_name = dict_sites[site_name]
    except KeyError:
        pass
    return site_name


def get_from_site(url):
    """"Gets html tags from web page, stores list of counts to db and returns the list of counts as json string"""
    logging.info('reading from site: ' + url)
    html_txt = get_html_txt(url)
    tags = html_tags(html_txt)
    tags_count = word_frequency(tags)
    tags_count_json = json.dumps(tags_count)

    return tags_count_json


def init_logging(file_logs):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(filename=file_logs, mode='a'),
            logging.StreamHandler()
        ])


def run_console(args, dict_sites, db_session):
    tags_count_json = None
    if args['get']:
        url = select_synonym_from_dict(args['get'], dict_sites)
        tags_count_json = get_from_site(url)
        write_to_db(url, tags_count_json, db_session)
    elif args['view']:
        url = select_synonym_from_dict(args['view'], dict_sites)
        tags_count_json = view_from_db(url, db_session)
    else:
        print("url was not provided via neither of the args: --get, --view")
    if tags_count_json:
        print(json.dumps(json.loads(tags_count_json), indent=2))


def run_ui(db_session):
    master = tk.Tk()
    app = MainWindowGUI(master, db_session, get_from_site, view_from_db, write_to_db)
    master.mainloop()

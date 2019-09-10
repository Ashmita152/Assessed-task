#!/usr/bin/python3

import os
import re
import sys
import string
import logging
import argparse
import traceback
import wikipedia

def search_wiki(keyword, count):
    """
    Searches a keyword in wikipedia database
    """
    try:
        result = wikipedia.search(keyword, count)
    except Exception:
        logging.error(traceback.format_exc())
    return result

def get_wiki(title):
    """
    Gets content of a wikipedia page
    """
    try:
        page = wikipedia.page(title)
    except Exception:
        logging.error(traceback.format_exc())
    return page.content

def create_dir(keyword):
    """
    Create the directory for storing the wiki pages
    """
    try:
        os.makedirs(keyword)
    except OSError:
        pass
    except Exception:
        logging.error(traceback.format_exc())

def write_file(path, content):
    """
    Write content to file
    """
    try:
        fd = os.open(path, os.O_CREAT|os.O_WRONLY)
        os.write(fd, content.encode())
    except Exception:
        logging.error(traceback.format_exc())
    finally:
        os.close(fd)

def sanitize_title(name):
    """
    Cleanup the filename
    """
    name = name.replace(" ", "_")
    for char in ["(", ")", "'"]:
        if char in name:
            name = name.replace(char, "")
    return name

def sanitize_content(content):
    """
    Sanitize the content
    1. Add choi notation.
    2. Remove punctuations.
    3. Remove empty lines.
    """
    content = re.sub(r"==.*==", "==========", content)
    table = str.maketrans({key: None for key in string.punctuation.replace('=','').replace('.','')})
    content = content.translate(table).replace('. ','\n').replace('.','\n').strip()
    content = os.linesep.join([s for s in content.splitlines() if s])
    return content

def attach_files(path):
    """
    Attaches all files of path into single file
    """
    try:
        fo = os.open(path+".txt", os.O_CREAT|os.O_WRONLY) 
        for _, _, files in os.walk(path):
            for file in files:
                fi = open(path+"/"+file, "r")
                for line in fi.readlines():
                    os.write(fo, line.encode())
    except Exception:
        logging.error(traceback.format_exc())
    finally:
        os.close(fo)

def read_input():
    """
    Reads input parameters
    """
    parser = argparse.ArgumentParser(description='Wikipedia Data Scraper')
    parser.add_argument(
        '--search', 
        dest='search',
        type=str,
        default='football,cricket',
        help='comma-separated list of keywords to search in wikipedia'
    )
    parser.add_argument(
        '--results',
        dest='results',
        type=int,
        default=10,
        help='maximum number of results returned for each wikipedia search'
    )
    args = parser.parse_args()
    return args

def main():
    """
    Wikipedia Scraper Entrypoint
    """
    args = read_input()
    results, keywords = args.results, args.search

    ## create a hashmap to map keyword and wiki titles corresponding to that keyword
    keyword_wiki = {}
    for keyword in keywords.split(","):
        search_result = search_wiki(keyword, results)
        keyword_wiki[keyword] = search_result

    ## layout the filesystem with proper directory structure
    for keyword in keywords.split(","):
        create_dir(keyword)

    ## get the content of wiki titles and store it in files
    for keyword, titles in keyword_wiki.items():
        for title in titles:
            content = sanitize_content(get_wiki(title))
            path = keyword + "/" + sanitize_title(title) + ".txt"
            write_file(path, content)

        ## append all files for a keyword into single file
        attach_files(keyword)

if __name__ == '__main__':
    sys.exit(main())

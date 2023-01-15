#!/usr/bin/env python3
import logging
import re
import sys
import types
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup


def checkUrl(url):
    parts = urlparse(url)
    fragment=parts.fragment
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        logging.error(f"Connection failed for {url}")
        return 1
    if not response.ok:
        logging.error(f"status {response.status_code} returned for {url}")
        return 1
    if response.url != url:
        logging.warning(f"got redirected to {response.url} from {url}")
    htmlDocument=response.text
    if fragment:
        logging.debug(f"fragment is \"{fragment}\"") 
        soup = BeautifulSoup(htmlDocument, 'html.parser')
        htmlElements=soup.find_all(id=fragment)
        if len(htmlElements)==0:
            # Not an id, trying name
            htmlElements=soup.find_all(name=fragment)        
        if len(htmlElements)==0:
            logging.error(f"fragment \"{fragment}\" not found in {url}")
            return 1
        logging.debug(f"found fragment \"{fragment}\"") 
    logging.info(f"no issues with {url}")
    return 0

def checkCheckUrls(check):
    urlErrors=0
    # Check URLs in remediation text
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    if not check['remediation']:
        logging.info("Check has no remediation section, skipping check")
        return 0
    urls = re.findall(regex, check['remediation'])
    logging.debug(f"{len(urls)} URLs found")
    if len(urls)>0:
        for url in urls:
            urlErrors += checkUrl(url[0])
    return urlErrors

def checkCheck(check):
    checkErrors=0
    logging.info(f"checking check {check['id']}")
    checkErrors+=checkCheckUrls(check)
    return checkErrors

def getChecksfromCheckFile(filename):
    logging.debug(f"processing file {filename}")
    checks=[]
    try:
        with open(filename, 'r') as file:
            docs = yaml.safe_load_all(file)
            if not isinstance(docs, types.GeneratorType):
                logging.warning(f"file \"{filename}\" contains no valid YAML documents, skipping")
                return
            for check in docs:
                if not check['id']:
                    logging.debug("Check has no id property, skipping")
                    continue
                checks.append(check)
    except FileNotFoundError:
        logging.debug(f"file \"{filename}\" not found, skipping")
    logging.debug(f"found {len(checks)} checks in file \"{filename}\"")
    return checks

if __name__ == "__main__":
    logformat='%(levelname)s: %(message)s'
    logging.basicConfig(level=logging.WARNING, format=logformat)
    #logging.basicConfig(level=logging.DEBUG, format=logformat)

    allErrors=0
    # Check all files given as parameters
    for _, arg in enumerate(sys.argv[1:]):
        checks=getChecksfromCheckFile(arg)
        for check in checks:
            allErrors += checkCheck(check)
    
    logging.shutdown()
    exit(int(allErrors > 0))

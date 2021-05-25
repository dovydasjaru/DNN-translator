from urllib.error import URLError
import requests
from bs4 import BeautifulSoup
import urllib.request
import time


wikipedia_page_format = "https://{0}.wikipedia.org/w/api.php"
# Query for wikipedia
# Titles and language links are omitted, need to add before query
wikipedia_query_params = {
    "action": "query",
    "prop": "extracts|iwlinks|pageprops|langlinks",
    "exintro": "true", "explaintext": "true",  # Extracts properties
    "iwprefix": "wikidata",  # IwLinks properties
    "ppprop": "disambiguation",  # PageProps properties
    "lllang": "",  # LangLinks properties
    "titles": "",
    "redirects": "true",
    "format": "json"
}


def make_request(title: str, target_language: str, source_language: str) -> dict:
    time.sleep(1)
    wikipedia_query_params['titles'] = title
    wikipedia_query_params['lllang'] = target_language
    response = requests.get(wikipedia_page_format.format(source_language), params=wikipedia_query_params)
    page = response.json()['query']['pages'].popitem()
    if 'missing' in page[1]:
        return {"result": ""}
    if 'disambiguation' in page[1].get('pageprops', {}):
        return {"result": page[1]['title']}
    if 'langlinks' in page[1]:
        return {"result": page[1]['langlinks'][0]['*'], "translated": ""}
    if 'iwlinks' in page[1]:
        common_name = __get_wiki_data_common_name(page[1]['iwlinks'][0]['*'], target_language)
        if common_name != "":
            return {"result": common_name, "translated": ""}
    return {"result": f"{page[1]['title']}: {page[1]['extract']}"}


def __validate_tag(tag):
    return tag.name == "span" or tag.name == "div"


def __get_wiki_data_common_name(wiki_data_page: str, language_code: str) -> str:
    wiki_page = "https://www.wikidata.org/wiki/"
    request = urllib.request.Request(wiki_page+wiki_data_page, headers={'User-Agent': "Magic Browser"})
    try:
        page_result = urllib.request.urlopen(request)
    except URLError:
        return ""
    data = page_result.read()
    soup = BeautifulSoup(data, features="lxml")
    soup = soup.find(id="mw-content-text")
    for common_name in soup.find_all(__validate_tag, {"lang": language_code}, recursive=True, limit=1):
        return common_name.string
    return ""

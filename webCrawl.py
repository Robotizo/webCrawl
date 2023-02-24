import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession


output1 = []
listItem = {
    'title': '',
    'link': '',
    'email': [],
    'phone': []
}


def get_source(url):
    try:
        session = HTMLSession()
        r = session.get(url)
        # print(r.html.links)
        return r

    except requests.exceptions.RequestException as e:
        print(e)


def get_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    # print(response.html.links)
    return response


def get_results_link(url):
    response = get_source(url)
    return response


def get_from_site(site):
    response = get_source(site)
    results = response.html.find("a", containing='@')
    return results


def get_from_site_phone(site):
    response = get_source(site)
    results = response.html.find(
        "a", containing=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    return results


def parse_results(response):
    output = []

    css_identifier_title = "h3"
    css_identifier_result = ".tF2Cxc"
    css_identifier_link = ".yuRUbf a"

    results = response.html.find(css_identifier_result)

    for result in results:
        listItem['title'] = result.find(css_identifier_title, first=True).text
        listItem['link'] = result.find(
            css_identifier_link, first=True).attrs['href']
        res = get_from_site(listItem['link'])
        listItem['email'] = res
        phone = get_from_site_phone(listItem['link'])
        listItem['phone'] = phone

        output.append(listItem)
        print('/n')
        print('/n')
        print('/n')
        print(listItem)
        print('/n')
        print('/n')
        print('/n')

    return output


def all_pages(response):
    css_identifier_sublink = "a.fl"
    links = response.html.find(css_identifier_sublink)
    rest_link = []
    print(links)

    for paginatedLink in links[:3]:
        link_item = {
            'link': 'https://www.google.com' + paginatedLink.find(css_identifier_sublink, first=True).attrs['href'],
        }
        rest_link.append(link_item)
    return rest_link


def google_search(query):
    response = get_results(query)
    parse_results(response)
    pages = all_pages(response)
    for subLink in pages:
        subresponse = get_results_link(subLink['link'])
        parse_results(subresponse)


google_search('canadian verterans health resources')

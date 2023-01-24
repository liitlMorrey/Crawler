from bs4 import BeautifulSoup
import requests


#standard browswr simulieren, durch einfügen eines Headers in den HTTP-Request
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}


def crawlSiteForSpecificWord(url, word):
    #HTTP Request an URL senden und antwort als Variable 'html' speichern
    html = requests.get(url, headers=headers)

    #html in BeautifulSoup Objekt parsen und als bs in Variable speichern
    bs = BeautifulSoup(html.content, "html.parser")
    #extrahiert Text aus HTML und splittet wörter in liste
    words = bs.get_text().split()

    #gesuchtes wort definieren und zählen
    word_filter = word.lower()
    counter = 0
    for word in words:
        if word.lower() == word_filter:
            counter += 1

    return counter

def getLinksOfSite(url):
    # HTTP Request an URL senden und antwort als Variable 'html' speichern
    html = requests.get(url, headers=headers)

    # html in BeautifulSoup Objekt parsen und als bs in Variable speichern
    bs = BeautifulSoup(html.content, "html.parser")

    body = bs.body

    baseUrl = getBaseUrl(url)

    linkList = []
    for link in body.find_all('a'):
        try:
            linkList.append(baseUrl + link.get('href'))
        except:
            print("Fehler: link.get('href') gibt ", link.get('href'))
    return linkList

def getBaseUrl(url):
    indexOfDomain = url.find('.de')
    return url[:indexOfDomain+3]

def ultimateSearch(url, word):
    allLinks = getLinksOfSite(url)
    print(allLinks)
    ultimateCounter = 0
    for link in allLinks:
        try:
            print("Link found " + link)
            counterOfUnderpage = crawlSiteForSpecificWord(link, word)
            print(counterOfUnderpage)
            ultimateCounter += counterOfUnderpage
        except:
            print("Link kaputt")
            continue
    print(ultimateCounter)

link = "https://unterrichten.zum.de/wiki/Geschichte"
wort = "Er"

ultimateSearch(link, wort)
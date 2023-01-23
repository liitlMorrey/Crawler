from bs4 import BeautifulSoup
import requests
import requests
import ssl


def crawlSiteForSpecificWord(url, word):
    #standard browswr simulieren, durch einfügen eines Headers in den HTTP-Request
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    #HTTP Request an URL senden und antwort als Variable 'html' speichern
    html = requests.get(url, headers=headers)

    #html in BeautifulSoup Objekt parsen und als bs in Variable speichern
    bs = BeautifulSoup(html.content, "html.parser")
    #extrahiert Text aus HTML und splittet wörter in liste
    words = bs.get_text().split()
    # <a href="link">Text</a>
    linkTags = bs.find_all('a')
    for linkTag in linkTags:
        linkWords = linkTag.get_text().split()
        words.append(linkWords)

    #wgesuchtes ort definieren und zählen
    word_filter = word
    counter = 0
    for word in words:
        if word == word_filter:
            counter += 1

    return counter

def getLinksOfSite(url):
    # standard browswr simulieren, durch einfügen eines Headers in den HTTP-Request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    # HTTP Request an URL senden und antwort als Variable 'html' speichern
    html = requests.get(url, headers=headers)

    # html in BeautifulSoup Objekt parsen und als bs in Variable speichern
    bs = BeautifulSoup(html.content, "html.parser")

    body = bs.body

    baseUrl = getBaseUrl(url)

    linkList = []
    for link in body.find_all('a'):
        linkList.append(baseUrl + link.get('href'))

    return linkList

def getBaseUrl(url):
    indexOfDomain = url.find('.org')
    return url[:indexOfDomain+4]

def ultimateSearch(url, word):
    allLinks = getLinksOfSite(url)
    print(allLinks)
    ultimateCounter = 0
    for link in allLinks:
        try:
            print("Good link found " + link)
            counterOfUnderpage = crawlSiteForSpecificWord(link, word)
            print(counterOfUnderpage)
            ultimateCounter += counterOfUnderpage
        except:
            continue
    print(ultimateCounter)

ultimateSearch("https://de.khanacademy.org/math/algebra2/introduction-to-complex-numbers-algebra-2/the-complex-numbers-algebra-2/a/intro-to-complex-numbers", "Zahlen")
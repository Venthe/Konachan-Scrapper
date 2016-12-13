import urllib.request
import urllib.parse
import os
import html
from bs4 import BeautifulSoup

targetLink = "http://konachan.com/post?page="
startingPage = 1
endingPage = 10

def cleanUrl(url):
    return urllib.parse.unquote(html.unescape(url)).strip()

def cleanFullFileName(imageHref):
    imageFullFileName = os.path.basename(imageHref)
    imageFullFileName = cleanUrl(imageFullFileName)
    imageFullFileName = os.path.splitext(imageFullFileName)
    return imageFullFileName
	
def removeReservedCharacters(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value;

def removeWindowsReservedCharacters(value):
    return removeReservedCharacters(value, '\/:*?"<>|')

def cleanImageFileName(imageFileName):
    imageFileName = imageFileName[15:] # remove "konachan.com - "
    imageFileName = removeWindowsReservedCharacters(imageFileName)
    imageFileName = imageFileName[:48] # limit length
    imageFileName = imageFileName.strip() # and clean
    return imageFileName

def getDirectLinksToImages(targetUrl):
    konachanWrapperId = "post-list-posts"
    konachanDirectLinkClass = "directlink"

    content = urllib.request.urlopen(targetUrl).read()
    soup = BeautifulSoup(content, 'html.parser')

    elementsWrapper = soup.find(id=konachanWrapperId)
    directLinksToImages = elementsWrapper.find_all("a", class_=konachanDirectLinkClass)
    return directLinksToImages

class ImageUrlWrapper:
    def __init__(self, image):
        imageHref = image.get("href")
        imageFullFileName = cleanFullFileName(imageHref)
        imageFileName = cleanImageFileName(imageFullFileName[0])
        imageFileExt = imageFullFileName[1]
        fileNameConcatenate = imageFileName+imageFileExt

        self.url = imageHref
        self.fileName = fileNameConcatenate

def listImagesInUrl(targetUrl):
    directLinksToImages = getDirectLinksToImages(targetUrl)
    for image in directLinksToImages:
        img = ImageUrlWrapper(image)

        print("  Storing: " + img.fileName)
        urllib.request.urlretrieve(img.url, img.fileName)
    return

def scrapKonachanImages(targetUrl, startingPageNo, endingPageNo): 
    currentPageNo = startingPageNo
    while True:
        currentUrl = targetUrl + str(currentPageNo)
        print("Targetting: " + currentUrl)
        listImagesInUrl(currentUrl)
        print()
        currentPageNo = currentPageNo + 1
        if(currentPageNo > endingPageNo): return

scrapKonachanImages(targetLink, startingPage, endingPage)
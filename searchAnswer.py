import urllib,urllib2
from BeautifulSoup import BeautifulSoup
from PIL import Image
from pytesseract import image_to_string
import requests

def bingSearch(query):
    address = "http://www.bing.com/search?q=%s" % (urllib.quote_plus(query))

    getRequest = urllib2.Request(address, None, {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'})

    urlfile = urllib2.urlopen(getRequest)
    htmlResult = urlfile.read()
    urlfile.close()
    soup = BeautifulSoup(htmlResult)
    [s.extract() for s in soup('span')]
    unwantedTags = ['a', 'strong', 'cite']
    for tag in unwantedTags:
        for match in soup.findAll(tag):
            match.replaceWithChildren()

    results = soup.findAll('li', attrs={ "class" : "b_algo" })
    everything = []
    for result in results:
        everything.append(str(result.find('p')))
        everything.append(str(result.find('tbody')))
    return everything

# new = phrase
def wordOrSent(number, question, new, track, answer):
    try:
        hi = new[number].split(" ")
        hi[1]
        claim = True
 
    except:
        claim = False
        line = new[number]
        n = len(line)/2
        line = [line[i:i + n] for i in range(0, len(line), n)]

    for phrase in answer:
        if new[number] in str(phrase) or new[number].lower() in str(phrase):
            track += 1
        if claim is True:
            for part in hi:
                if part.lower() in question.lower():
                    break
                if part in phrase:
                    track += 1
        if claim is False:
            for part in line:
                if part.lower() in question.lower():
                    break
                if part in phrase:
                    track += 1
    return track


def main():
    new = []
    img = Image.open('sc.png')

    myText = image_to_string(img, config='-c tessedit_char_whitelist=01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.?\"\"\'\'')
    myText = myText.encode('ascii', 'ignore')
    try:
        separate = myText.split("?")
    except:
        separate = myText.split("\n\n")

    separate[0]= separate[0].replace("\n", " ")
    for line in separate:
        new.append(line)
    new[0]=new[0][3:]
    question = new[0] + "?"

    no = ["NOT", "not"]
    stopwords = ['the','that','a','in','not','an','has']
    querywords = question.split()
    resultwords  = [word for word in querywords if word.lower() not in stopwords]

    if no in querywords:
        print("NOTNOTNOTNOTNOT")
    result = ' '.join(resultwords)

    answer = bingSearch(result)
    new = new[1:]
    new = " ".join(new)
    new = new.strip()
   
    new = new.split("\n")
    print(new)
    for item in new:
        if not item:
            new.remove(item)
    print(new)

    track1 = 0
    track2 = 0
    track3 = 0

    track1 = wordOrSent(0, question, new, track1, answer)
    track2 = wordOrSent(1, question, new, track2, answer)
    track3 = wordOrSent(2, question, new, track3, answer)


    total = track1 + track2 + track3
    total = float(total)
    try:
        print(str(track1/total*100)+"%")
        print(str(track2/total*100)+"%")
        print(str(track3/total*100)+"%")
    except:
        print(track1)
        print(track2)
        print(track3)

main()

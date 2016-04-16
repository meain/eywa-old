import urllib
from bs4 import BeautifulStoneSoup, BeautifulSoup #import beautifulsoup4 #Extra dependency (install it using pip) (used for parsing a single tag and also to encode the string to unicode format)
import cgi

# call = urllib.urlopen("https://docs.python.org/2/library/urllib.html")
# data = call.read()
# print data

api_key = "VWL342-QUTHXQJQR6" #Wolfram alpha calls them appID

# def HTMLEntitiesToUnicode(text): # Uses beautifulsoup4
    # """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    # text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    # return text

def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
    return text

def frame_querry(querry):
    '''
    This funciton is used to crete a querry as an html request.
    '''
    api_request_base = "http://api.wolframalpha.com/v2/query?input="

    # Convert the queery to unicode
    converted_querry = unicodeToHTMLEntities(querry)

    # Create the queery
    final_querry = api_request_base + converted_querry + "&appid=" + api_key + "&format=plaintext"

    return final_querry

def make_request(querry):
    '''
    The returned data is an xml file, the main data content of the returned result is in the <plaintext> tag
    The fucntion extract just that part using beautifulsoup4(extra dependeny)  and returns the it as string
    '''
    result = urllib.urlopen(querry)
    data = result.read()
    print data

    #Extracting the exact answer to the querry using Beautifulsoup
    soup = BeautifulSoup(data, 'html.parser')
    dat = soup.find('pod', title = 'Result')
    if soup.queryresult['success'] == 'false':
        if soup.queryresult.didyoumeans:
            exact_result = "Did you mean : " + str(soup.queryresult.didyoumeans.didyoumean)
        elif soup.tips:
            exact_result = soup.queryresult.tips.tip['text']
        else:
            exact_result = "Unfortunately, we could not retrive data on it."
    elif soup.queryresult['success'] == 'true':
        exact_result = str(dat.plaintext.string)
    else:
        exact_result = "Unfortunately, we could not retrive data on it."
    return data, exact_result # Data includes the complete xml data that is returned by wolfram alpha and exact_result contains just the answer

def frame_and_request(querry):
    return make_request(frame_querry(querry))


'''
querry = "Who the American President?"
result,dat = frame_and_request(querry)
print result
print "\n\nResult : "
print dat
'''

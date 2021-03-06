'''
Handles wolframalpha api calls
'''
import urllib
import unicodedata
from bs4 import BeautifulStoneSoup, BeautifulSoup
import cgi

api_key = "VWL342-QUTHXQJQR6" #Wolfram alpha calls them appID

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
    if dat:
        pass
    else:
        dat = soup.find('pod', title = 'Input interpretation')
    if soup.queryresult['success'] == 'false':
        if soup.queryresult.didyoumeans:
            exact_result = "Did you mean : " + str(soup.queryresult.didyoumeans.didyoumean)
        elif soup.tips:
            exact_result = soup.queryresult.tips.tip['text']
        else:
            exact_result = "Unfortunately, we could not retrive data on it."
    elif soup.queryresult['success'] == 'true':
        exact_result = str(unicodedata.normalize('NFKD', dat.plaintext.string).encode('ascii','ignore')
)
    else:
        exact_result = "Unfortunately, we could not retrive data on it."
    return data, exact_result # Data includes the complete xml data that is returned by wolfram alpha and exact_result contains just the answer

def frame_and_request(querry):
    return make_request(frame_querry(querry))

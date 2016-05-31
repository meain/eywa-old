from apis.aimlbot import *
import apis.wolframapi as wapi
import apis.imageapi as iapi

def check_if(query, text):
    if query == text:
        return True
    else:
        return False

def check_if_arg(query, text):
    if query.split(' ', 1)[0] == text and len(query.split(' ', 1)) > 1:
        return True
    else:
        return False

def get_query_arg(query):
    return query.split(' ', 1)[1]

def text_result(text):
    item = {}
    item['content'] = text
    item['type'] = "text"
    return item

def image_result(query):
    item ={}
    wsuccess, wlink = iapi.get_image(query)
    if wsuccess == True:
        item['content'] = wlink
        item['type'] = "image"
    else:
        item['content'] = 'No image'
        item['type'] = "text"
    return item


def wolfram_result(query):
    item = {}
    wresult,wdat = wapi.frame_and_request(query)
    item['content'] = wdat
    item['type'] = "text"
    return item

def aiml_result(query, k):
    item = {}
    # the aiml takes time to load, will have to run it in a parallel thread
    # item['content'] = "Not connected to aiml!"
    item['content'] = reply_aiml(query,k)
    if item['content'] == '':
        item['content'] = 'Issue with aiml'
    item['type'] = 'text'
    return item

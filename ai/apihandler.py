'''
This file is what handles all the formatting of the api data recived
On incoming request the apihandler queries the corresping base level api and retuns a formated result back
'''
from apis.aimlbot import *
import apis.wolframapi as wapi
import apis.imageapi as iapi

def text_result(text):
    '''
    Basic test result
    '''
    item = {}
    item['content'] = text
    item['type'] = "text"
    return item

def image_result(query):
    '''
    Result is a link to image, or in case no image is available it returns a text saying No Image
    '''
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
    '''
    Queries wolfram alpha api
    '''
    item = {}
    wresult,wdat = wapi.frame_and_request(query)
    item['content'] = wdat
    item['type'] = "text"
    return item

def aiml_result(query):
    '''
    Handles aiml queries
    '''
    item = {}
    item['content'] = reply_aiml(query)
    if item['content'] == '':
        item['content'] = 'Didn\'t get you'
    item['type'] = 'text'
    return item

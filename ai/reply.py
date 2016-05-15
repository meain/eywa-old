from aimlbot import *
import wolframapi as wapi
import imageapi as iapi

def get_result(query, user_id, k):
    res = []
    item = {}
    '''
    This fucniton diverts the querry to different routes
    Returns the result and the type of result
    '''
    if query == "hey":
        #return ("Hey " + user_id), "text"
        item['content'] = "Hey " + user_id
        item['type'] = "text"
        res.append(item)
        return res
    elif query.split(' ', 1)[0] == 'wolfram':
        query = query.split(' ', 1)[1]
        print "Wolfram query : " + query
        wresult,wdat = wapi.frame_and_request(query)
        #return wdat, "wolfram"
        item['content'] = wdat
        item['type'] = "text"
        res.append(item)
        return res
    elif query.split(' ', 1)[0] == 'image':
        query = query.split(' ', 1)[1]
        print "Image query : " + query
        wsuccess, wlink = iapi.get_image(query)
        if wsuccess == True:
            #return wlink, "image"
            item['content'] = wlink
            item['type'] = "image"
        else:
            #return 'No image', "text"	#Hope it will never be used
            item['content'] = 'No image'
            item['type'] = "text"
            res.append(item)
            return res
    elif query.split(' ', 1)[0] == 'multiline':
        query = query.split(' ', 1)[1]
        if query == 'ii':
            wsuccess, wlink = iapi.get_image('one')
            if wsuccess == True:
                #return wlink, "image"
                item['content'] = wlink
                item['type'] = "image"
            else:
                #return 'No image', "text"	#Hope it will never be used
                item['content'] = 'No image'
                item['type'] = "text"
                res.append(item)
                item = {}
                wsuccess, wlink = iapi.get_image('two')
                if wsuccess == True:
                    #return wlink, "image"
                    item['content'] = wlink
                    item['type'] = "image"
                else:
                    #return 'No image', "text"	#Hope it will never be used
                    item['content'] = 'No image'
                    item['type'] = "text"
                    res.append(item)
        elif query == 'it':
            wsuccess, wlink = iapi.get_image('placeholder')
            if wsuccess == True:
                #return wlink, "image"
                item['content'] = wlink
                item['type'] = "image"
            else:
                #return 'No image', "text"	#Hope it will never be used
                item['content'] = 'No image'
                item['type'] = "text"
                res.append(item)
                item = {}
                item['content'] = 'Dummy text'
                item['type'] = "text"
                res.append(item)
        elif query == 'ti':
            item['content'] = 'Dummy text'
            item['type'] = "text"
            res.append(item)
            item = {}
            wsuccess, wlink = iapi.get_image('placeholder')
            if wsuccess == True:
                #return wlink, "image"
                item['content'] = wlink
                item['type'] = "image"
            else:
                #return 'No image', "text"	#Hope it will never be used
                item['content'] = 'No image'
                item['type'] = "text"
                res.append(item)
        elif query == 'tt':
            item['content'] = 'Dummy text one'
            item['type'] = "text"
            res.append(item)
            item = {}
            item['content'] = 'Dummy text two'
            item['type'] = "text"
            res.append(item)
        return res
    else :
        # the aiml takes time to load, will have to run it in a parallel thread
        item['content'] = reply_aiml(query,k)
        item['type'] = 'text'
        res.append(item)
        return res
'''
get the user id then we can use it from the python insterface so as to get the information from the google server by querrying with the id
a possible problem is that our python app wont be able queey directly -
-- either register python app and chang the whole login thing into python
-- or pipe python querry through the html server ;)
'''

from apihandler import *

def check_if(query, text):
    # Just check for simple text match
    if query == text:
        return True
    else:
        return False

def check_if_arg(query, text):
    # checking everything from second word
    if query.split(' ', 1)[0] == text and len(query.split(' ', 1)) > 1:
        return True
    else:
        return False

def get_query_arg(query):
    # Get all except first word from user query
    return query.split(' ', 1)[1]


def get_result(user_data):
    query = user_data['msg']
    result = []
    '''
    This funciton diverts the querry to different routes
    Mostly hardcoded stuff here as of now, but once NLP is implemented we could replace this
    Returns the result and the type of result
    '''
    if check_if(query, "hey") :
        result.append(text_result("Hey " + user_data['name']))
    elif check_if_arg(query, "wolfram") :
        print "Wolfram query : " + query
        # Calls Wolfram Alpha api, the result returned back is a dict
        result.append(wolfram_result(get_query_arg(query)))
    elif check_if_arg(query, "image") :
        print "Image query : " + query
        # Calls image api
        result.append(image_result(get_query_arg(query)))
        result.append(text_result("Here is an image of ' " + get_query_arg(query) + " '"))
    else :
        print "Aiml query : " + query
        # Uses aiml if none above works
        result.append(aiml_result(query))
    # Return the result
    return result

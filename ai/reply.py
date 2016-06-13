from apihandler import *

def get_result(query, user_name, k):
    res = []
    '''
    This fucniton diverts the querry to different routes
    Returns the result and the type of result
    '''
    if check_if(query, "hey"):
        res.append(text_result("Hey " + user_name))
        return res
    elif check_if_arg(query, "wolfram"):
        print "Wolfram query : " + query
        res.append(wolfram_result(get_query_arg(query)))
        return res
    elif check_if_arg(query, "what"):
        print "What : " + query
        res.append(image_result(get_query_arg(query)))
        res.append(wolfram_result(get_query_arg(query)))
        return res
    elif check_if_arg(query, "image"):
        print "Image query : " + query
        res.append(image_result(get_query_arg(query)))
        res.append(text_result("Here is an image of ' " + get_query_arg(query) + " '"))
        return res
    elif check_if_arg(query, "multiline"):
        print "Multiline check"
        arg = get_query_arg(query)
        if arg == 'ii':
            res.append(image_result("one"))
            res.append(image_result("two"))
        elif arg == 'it':
            res.append(image_result("placeholder"))
            res.append(text_result("Dummy text"))
        elif arg == 'ti':
            res.append(text_result("Dummy text"))
            res.append(image_result("placeholder"))
        elif arg == 'tt':
            res.append(text_result("Dummy text one"))
            res.append(text_result("Dummy text two"))
        return res
    else :
        print "Aiml query : " + query
        res.append(aiml_result(query, k))
        return res

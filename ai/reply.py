from aimlbot import *
def get_result(query, user_id, k):
    if query == "hey":
        return "Hey " + user_id
    else:
        # the aiml takes time to load, will have to run it in a parallel thread
        return reply_aiml(query, k)
'''
get the user id then we can use it from the python insterface so as to get the information from the google server by querrying with the id
a possible problem is that our python app wont be able queey directly -
    -- either register python app and chang the whole login thing into python
    -- or pipe python querry through the html server ;)
'''

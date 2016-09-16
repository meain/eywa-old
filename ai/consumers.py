from channels.handler import AsgiHandler
import json
import urllib
from reply import *
from models import Querry
from django.utils import timezone

def http_consumer(message):
    '''
    No http request has to be handled here.
    The only http request is before initiating ws, so is handled in views.py
    '''
    pass

def ws_message(message):
    '''
    Hnadles all the queries/chats
    '''
    # Extract user data
    usr_data = json.loads(message.content['text']) # Contains [msg, id, name, email, image]

    # Convert msg and id from unicode to sting
    urllib.unquote(usr_data['msg']).decode('utf8')
    urllib.unquote(usr_data['id']).decode('utf8')

    # Get result from reply.py
    q_res= get_result(usr_data)

    # Logging to database
    query_data = Querry(querry_term = usr_data['msg'], querry_result = q_res, timestamp = timezone.now())
    query_data.save()

    # Format result
    data = {}
    data['querry_term'] = query_data.querry_term
    data['resultsno'] = len(q_res)
    data['results'] = q_res

    # Display log
    print "\n\n---------------------"
    print "User message : " + usr_data['msg'] + "\nUser id : "  + usr_data['id']
    print "Result : \n" + str(data['results'])
    print "---------------------------\n\n"

    # Reply back to the websocket query
    data = json.dumps(data)
    message.reply_channel.send({
        "text": data,
    })

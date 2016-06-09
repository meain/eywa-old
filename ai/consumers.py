from django.http import HttpResponse
from channels.handler import AsgiHandler
import json
import urllib
from reply import *
from models import Querry
from django.utils import timezone

def http_consumer(message):
    pass

def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    usr_data = json.loads(message.content['text'])
    msg = usr_data['msg']
    id = usr_data['id']
    name = usr_data['name']
    email = usr_data['email']
    image = usr_data['image']
    print "\n\n---------------------"
    print "User message : " + msg + "\nUser id : "  + id + "\n"
    # it is currently in unicode format and has to be converted into string
    urllib.unquote(msg).decode('utf8')
    urllib.unquote(id).decode('utf8')
    k = ''
    q_res= get_result(msg, name, k)
    q = Querry(querry_term = msg, querry_result = q_res, timestamp = timezone.now())
    q.save()
    print "Result : \n" + str(q_res)
    data = {}
    data['querry_term'] = q.querry_term
    data['resultsno'] = len(q_res)
    data['results'] = q_res
    data = json.dumps(data)
    print "\nJson response : \n" + data
    print "---------------------------\n\n"
    message.reply_channel.send({
        "text": data,
    })

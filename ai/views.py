from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from models import Querry
from serializers import AiSerializer
from django.core import serializers
from django.utils import timezone
import json
import urllib
import threading
from multiprocessing import Queue

# Create your views here.
from reply import *
from aimlbot import *
k = ''
from .forms import QuerryForm

# ========================================================================================
# ========================================================================================
#You will be editing this funciton to get things done
#This automaticlaly save all the querries and th results generated into a databese jsut in case it is necesary
#Stuff backed up to the database:
    # querry_term
    # querry_result
    # timestamp
#You dont have to worry about anything, all you have to do is to make this "customFunciton" which gets the,
#user querry as the variable "term" and get the output and return it
#as a string(currently, will change that model if json or something like that is what you want as the result).
'''change in reply.py'''
# ========================================================================================
# ========================================================================================

def load_aiml():
    global k
    # k = initialize_aiml()
    print "Still loading"

def index(request):
    form = QuerryForm(request.POST or None)
    context = {'form' : form}
    aiml_thread = threading.Thread(target=load_aiml())
    aiml_thread.start()
    return render(request, "ai/index.html", context)

class QuerryResult(generics.RetrieveUpdateDestroyAPIView):
    queryset = Querry.objects.all()
    serializer_class = AiSerializer

def reply(request):
    if request.method == 'POST':
       msg = request.POST['umsg']
       id = request.POST['uid']
       name = request.POST['uname']
       email = request.POST['uemail']
       image = request.POST['uimage']
       print "\n\n------------------------------------------------------------------"
       print "User message : " + msg + "\nUser id : "  + id + "\n"
       # it is currently in unicode format and has to be converted into string
       urllib.unquote(msg).decode('utf8')
       urllib.unquote(id).decode('utf8')
       global k
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
       print "------------------------------------------------------------------\n\n"
       return HttpResponse(data, content_type='application/json')
       return HttpResponse('')





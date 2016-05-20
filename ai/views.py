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

def index(request):
    form = QuerryForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        print instance.querry_term

        #This is what you will hve to edit
        instance.querry_result = customFuncion(instance.querry_term)

        instance.save()
        # return redirect('result', instance)
        return render(request, "ai/result.html", {'querry' : instance})
    else:
        print "Not valid"
        global k
        # k = initialize_aiml()
    context = {'form' : form}
    return render(request, "ai/index.html", context)

class QuerryResult(generics.RetrieveUpdateDestroyAPIView):
    queryset = Querry.objects.all()
    serializer_class = AiSerializer

def ajax_view(request, msg, idu):
    print msg + "\n"  + idu
    # it is currently in unicode format and has to be converted into string
    urllib.unquote(msg).decode('utf8')
    urllib.unquote(idu).decode('utf8')
    global k
    q_res= get_result(msg, idu, k)
    q = Querry(querry_term = msg, querry_result = q_res, timestamp = timezone.now())
    q.save()
    print q_res
    data = {}
    data['querry_term'] = q.querry_term
    data['resultsno'] = len(q_res)
    data['results'] = q_res
    data = json.dumps(data)
    print data
    print '.'
    print str(data)
    return HttpResponse(data, content_type='application/json')

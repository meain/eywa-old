from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from models import Querry
from serializers import AiSerializer
from django.core import serializers
from django.utils import timezone
import json
import urllib

# Create your views here.

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
def custom_function(term):
    return "result data"
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
    context = {'form' : form}
    return render(request, "ai/index.html", context)
# def result(request):
#     form = QuerryForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit = False)
#         print instance.querry_term
#         # Do your thing here
#         ##
#
#
#
#         ##
#         instance.save()
#         return redirect('index')
#     else:
#         print "Not valid"
#     context = {}
#     return render(request, "ai/result.html", context)

# def result(form):
#     # print pk
#     context = {}
#     return render(request, "ai/result.html", context)

class QuerryResult(generics.RetrieveUpdateDestroyAPIView):
    queryset = Querry.objects.all()
    serializer_class = AiSerializer

def ajax_view(request, msg, idu):
    print msg + "\n"  + idu
    pk = msg
    # it is currently in unicode format nd has to converted into string
    urllib.unquote(pk).decode('utf8')
    # print "booo"
    q_res = custom_function(pk)
    # print q_res
    q = Querry(querry_term = pk, querry_result = q_res, timestamp = timezone.now())
    q.save()
    # print q.querry_result
    data = serializers.serialize('json', [q])
    data = str(data)
    data = data[1:]
    data = data[:-1]
    print data
    # print data + "sdfsdqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    # print type(data[0])
    # print type(data)
    # print HttpResponse(data, content_type='application/json')
    return HttpResponse(data, content_type='application/json')
    # print JsonResponse(q, safe = False)
    # return JsonResponse(json.dumps(data))

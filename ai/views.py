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
from apis.aimlbot import *
k = ''
from .forms import QuerryForm

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

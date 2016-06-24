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
import aiml

# Create your views here.
from reply import *
from apis.aimlbot import *
k = initialize_aiml()
from .forms import QuerryForm
flag = 0

def get_aiml():
    global k
    return k

def index(request):
    form = QuerryForm(request.POST or None)
    context = {'form' : form}
    return render(request, "ai/index.html", context)


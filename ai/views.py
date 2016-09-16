from django.shortcuts import render, redirect
from apis.aimlbot import initialize_aiml

# Initializing aiml here helps to initialize aiml as soon as we start the server
initialize_aiml()

def index(request):	
	# Return the page at ai/index.html
	return render(request, "ai/index.html", None)


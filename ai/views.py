from django.shortcuts import render, redirect

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
def customFuncion(term):
    return term
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

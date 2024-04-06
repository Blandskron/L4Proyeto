from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Question
from .forms import QuestionForm

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('formsapp/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse("Estas buscando una pregunta %s." % question_id)

def results(request, question_id):
    response = "Estas buscando el resultado de una pregunta %s."
    return HttpResponse(response % question_id)
 
def vote(request, question_id):
    return HttpResponse("tu estas votando por una pregunta %s." % question_id)

def success(request):
    return render(request, 'formsapp/success.html')

def question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success') 
    else:
        form = QuestionForm()
    return render(request, 'formsapp/form.html', {"form": form})

def back_to_home(request):
    return redirect('index')

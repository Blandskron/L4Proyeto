# L4Proyeto

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
cd venv 
Scripts\activate
cd ..

# Instalar Django
pip install django

# Crear proyecto django
django-admin startproject forms

# Entrar al proyecto
cd forms

# Crear aplicacion
python manage.py startapp formsapp

# Incorporamos la aplicacion en nuestro archivo setting.py
INSTALLED_APPS = [
    'formsapp',
]

# Dentro de la carpeta formsapp Creamos un archivo llamado forms.py
from django import forms

class QuestionForm(forms.Form):
    text = forms.CharField()

# Incorporar una vista en views.py
from django.shortcuts import render
from .forms import QuestionForm

def question(request):
    form = QuestionForm()
    return render(request, 'formsapp/form.html', {"form": form})

# Crear archivo ursl.py tambien dentro d la carpeta de la aplicacion
from django.urls import path
from . import views

urlpatterns = [
    path('question/', views.question, name="question"),
]

# Creamos la carpeta templates y dentro otra carpeta llamada formsapp y creamos un archivo html form.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form</title>
</head>
<body>
    <form method="post" action="{% url 'question' %}">
        {% csrf_token %}
        <label for="id_question_text">Question Text:</label>
        <input type="text" id="id_question_text" name="question_text">
        <button type="submit">Guardar</button>
    </form>    
</body>
</html>



# Creamos las migraciones
python manage.py makemigrations formsapp
python manage.py migrate

# Ahora probamos que todo este bien levantando el proyecto
python manage.py runserver

# Luego cerramos el servidor para poder guardar la informacion del formulario en la base de datos
control + c

# Ahora modificamos el forms.py para conectar con la base de datos
from formsapp import models
from django import forms
from .models import Question

class QuestionForm(forms.Form):

    class Meta:
        model = Question
        fields = ("question_text")

    text = forms.CharField()

# Creamos el modelo para la base de datos modificando el models.py
from django.db import models
import datetime

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default = datetime.datetime.today)

    def __str__(self):
        return self.question_text
    
# Modificamos tambien el archivo views.py
from django.shortcuts import render
from .forms import QuestionForm

# Create your views here.
def question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
    form = QuestionForm()
    return render(request, 'formsapp/form.html', {"form": form})

# Creamos el super usuario
python manage.py createsuperuser

# Activamos las nuevas migraciones
python manage.py makemigrations formsapp
python manage.py migrate

# Ahora levantamos nuevamente el proyecto
python manage.py runserver




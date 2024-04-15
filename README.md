# L4Proyeto

# Crear entorno virtual
```
python -m venv venv
```
# Activar entorno virtual
```
cd venv 
Scripts\activate
cd ..
```
# Instalar Django
```
pip install django
```
# Crear proyecto django
```
django-admin startproject forms
```
# Entrar al proyecto
```
cd forms
```
# Crear aplicacion
```
python manage.py startapp formsapp
```
# Incorporamos la aplicacion en nuestro archivo setting.py
```
INSTALLED_APPS = [
    'formsapp',
]
```
# Dentro de la carpeta formsapp Creamos un archivo llamado forms.py
```
from django import forms

class QuestionForm(forms.Form):
    text = forms.CharField()
```
# Incorporar una vista en views.py
```
from django.shortcuts import render
from .forms import QuestionForm

def question(request):
    form = QuestionForm()
    return render(request, 'formsapp/form.html', {"form": form})
```
# Crear archivo ursl.py tambien dentro de la carpeta de la aplicacion
```
from django.urls import path
from . import views

urlpatterns = [
    path('question/', views.question, name="question"),
]
```
# Creamos la carpeta templates y dentro otra carpeta llamada formsapp y creamos un archivo html form.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        form {
            background-color: #fff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            margin: 0 auto;
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
        }
        button[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <form method="post" action="{% url 'question' %}">
        {% csrf_token %}
        <label for="id_question_text">Texto de la pregunta:</label>
        <input type="text" id="id_question_text" name="question_text" required>
        <button type="submit">Guardar</button>
    </form>
</body>
</html>
```
# Creamos las migraciones
```
python manage.py makemigrations formsapp
python manage.py migrate
```
# Ahora probamos que todo este bien levantando el proyecto
```
python manage.py runserver
```
# Luego cerramos el servidor para poder guardar la informacion del formulario en la base de datos
control + c

# Ahora modificamos el forms.py para conectar con la base de datos
```
from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("question_text",)
```
# Creamos el modelo para la base de datos modificando el models.py
```
from django.db import models
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default = datetime.datetime.today)

    def __str__(self):
        return self.question_text
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```    
# Modificamos tambien el archivo views.py
```
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
```
# Modificamos el archivo urls.py de la aplicacion
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('question/', views.question, name='question'),
    path('success/', views.success, name='success'),
    path('back-to-home/', views.back_to_home, name='back_to_home'),
]
```
# Modificamos el archivo de urls.py del proyecto
```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('formsapp/', include('formsapp.urls')),
]
```
# Creamos un archivo html para la respuesta del envio del formulario success.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario enviado con éxito</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        h1 {
            color: #4CAF50;
            text-align: center;
        }
        p {
            text-align: center;
        }
        a {
            display: block;
            width: 200px;
            margin: 20px auto;
            text-align: center;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>¡Formulario enviado con éxito!</h1>
    <p>Tu formulario ha sido procesado correctamente. Gracias por enviarlo.</p>
    <a href="{% url 'back_to_home' %}">
        <button>Volver a inicio</button>
    </a>
</body>
</html>
```
# Creamos el archivo html principal index.html
```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tus Preguntas</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            text-align: center;
            color: #4CAF50;
        }
        
        .questions {
            margin-top: 20px;
            text-align: center;
        }
        
        ul {
            list-style-type: none;
            padding: 0;
        }
        
        li {
            margin-bottom: 10px;
            background-color: #fff;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .no-questions {
            font-style: italic;
            color: #777;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tus Preguntas</h1>
        <div class="questions">
            {% if latest_question_list %}
                <ul>
                    {% for question in latest_question_list %}
                        <li>{{ question.question_text }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="no-questions">No hay preguntas.</p>
            {% endif %}
        </div>
        <a href="{% url 'question' %}"><button>Agregar preguntas</button></a>
    </div>
</body>
</html>
```
# Creamos el super usuario
```
python manage.py createsuperuser
```
# Activamos las nuevas migraciones
```
python manage.py makemigrations formsapp
python manage.py migrate
```
# Ahora levantamos nuevamente el proyecto
```
python manage.py runserver
```




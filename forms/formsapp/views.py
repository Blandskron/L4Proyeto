from django.shortcuts import render, redirect
from .forms import QuestionForm

def success(request):
    return render(request, 'formsapp/success.html')

def question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a una página de éxito después de guardar los datos
            return redirect('success')  # Reemplaza 'nombre_de_la_vista_de_exito' con el nombre de tu vista de éxito
    else:
        form = QuestionForm()
    return render(request, 'formsapp/form.html', {"form": form})



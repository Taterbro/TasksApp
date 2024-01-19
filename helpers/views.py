from django.shortcuts import render

def handlenotfound(request, exception):
    return render(request, 'todolist/notfound.html', status=404)

def custom500(request):
    return render(request, 'todolist/500.html', status=500)
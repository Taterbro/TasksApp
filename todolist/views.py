from django.shortcuts import render
from .forms import taskform
from .models import todoList
from django.http import HttpResponseRedirect 
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def showTodo(request, todos):
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'incomplete':
            return todos.filter(isCompleted = False)
        
        if request.GET.get('filter') == 'complete':
            return todos.filter(isCompleted = True)
        

    return todos

@login_required
def index(request):
    todos = todoList.objects.filter(owner=request.user.id)

    completecount=todos.filter(isCompleted=True).count()
    incompletecount=todos.filter(isCompleted=False).count()
    totalcount=todos.count()

    context = {'todos': showTodo(request, todos),
               'totalcount': totalcount,
               'completecount': completecount,
               'incompletecount': incompletecount,}
    

    return render(request, 'todolist/index.html', context)

@login_required
def addtask(request):
    form = taskform()
    context = {'form': form}

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        iscomp = request.POST.get('isCompleted', False)

        todo = todoList()
        todo.title = title
        todo.description = desc
        todo.isCompleted = True if iscomp == 'on' else False
        todo.owner = request.user

        todo.save()

        messages.add_message(request, messages.SUCCESS, 'Task added successfully')

        return HttpResponseRedirect(reverse('todolist', kwargs={'id':todo.pk}))
    
    return render(request, 'todolist/task.html', context)


@login_required
def todoDetails(request, id):
    todo = get_object_or_404(todoList, pk=id)
    context = {'todo': todo}
    return render(request, 'todolist/todoDetails.html', context)


@login_required
def todoDel(request, id):
    todo = get_object_or_404(todoList, pk=id)
    context = {'todo': todo}

    if request.method == 'POST':
        if todo.owner == request.user:
            todo.delete()

            messages.add_message(request, messages.SUCCESS, 'Task has been deleted')
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'todolist/todoDel.html', context)


@login_required
def edittask(request, id):
    todo = get_object_or_404(todoList, pk=id)
    form = taskform(instance=todo)

    context = {'todo': todo,
               'form': form}
    

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        iscomp = request.POST.get('isCompleted', False)

        todo.title = title
        todo.description = desc
        todo.isCompleted = True if iscomp == 'on' else False

        if todo.owner == request.user:
            todo.save()

            messages.add_message(request, messages.SUCCESS, 'Task has been updated')

            return HttpResponseRedirect(reverse('todolist', kwargs={'id':todo.pk}))
    
    return render(request, 'todolist/edittask.html', context)

# Create your views here.

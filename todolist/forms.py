from django import forms
from .models import todoList

class taskform(forms.ModelForm):

    class Meta:
        model = todoList

        fields = ['title', 'description', 'isCompleted']

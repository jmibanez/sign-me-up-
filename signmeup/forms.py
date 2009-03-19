from django import forms
from django.forms import fields
from django.forms import widgets

class TopicForm(forms.Form):
    name = fields.CharField(label = 'Name')
    description = fields.CharField(widget=widgets.Textarea, label='Short Description', 
                                   required=False)

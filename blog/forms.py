# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import  Comments

#Форма коментария
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment_text',)
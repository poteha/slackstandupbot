import json
from uuid import uuid4

from django import forms
from django.contrib import admin
from django.db import models
from .models import User, Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at',)
    list_display = ('text', 'order_number', 'is_active',)
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'cols': 50, 'rows': 1})},
    }


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at', 'answers',)
    list_display = ('name', 'is_active', 'channel_id', 'slack_id',)
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'cols': 50, 'rows': 1})},
    }
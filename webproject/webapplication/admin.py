from django.contrib import admin
from .models import Question,Choice
# Register your models here.

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['question_text'] } ),
        ('Data information', {'fields': ['pub_date'], 'class': ['collapse']}),
        ]

admin.site.register(Question, QuestionAdmin)

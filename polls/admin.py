from django.contrib import admin
from .models import Question,Choice



# Register your models here.
#admin.site.register(Question)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{"fields":["question_text"]}),
        ("Date Information",{"fields":["pub_date"]}),
    ]
    inlines =[ChoiceInline]
    list_display=["question_text", "pub_date","was_published_recently"]
    list_filter=["pub_date"]

admin.site.register(Question,QuestionAdmin)
#admin.site.register(Choice)
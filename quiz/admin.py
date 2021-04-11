from django.contrib import admin

from .models import Topic, Quiz, Question


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["question", "answer_a", "answer_b", "answer_c", "answer_d"]
    list_display = ["question", "quiz", "topic"]
    list_filter = ["quiz", "topic"]
    save_on_top = True


admin.site.register(Topic)
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)

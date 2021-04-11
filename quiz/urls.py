from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.QuizListView.as_view(), name="quiz-list"),
    path(
        "<int:pk>/",
        view=views.QuizDetailView.as_view(),
        name="quiz-detail",
    ),
]

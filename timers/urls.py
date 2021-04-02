from django.urls import path

from . import views

urlpatterns = [
    path("", views.TimersListView.as_view(), name="timers"),
    path("<slug:slug>/", views.TimerDetailView.as_view(), name="timer-detail"),
]

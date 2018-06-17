
from django.urls import path

from . import views

urlpatterns = [path("", views.TimersListView.as_view(), name="timers")]

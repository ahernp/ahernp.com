from django.urls import path

from . import views

urlpatterns = [
    path("", views.ToolsView.as_view(), name="tools"),
    path("<slug:tool>/", views.ToolsView.as_view(), name="tool"),
]

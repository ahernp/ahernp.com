from django.urls import path

from . import views

urlpatterns = [path("", views.ProductFeedListView.as_view(), name="dashboard")]

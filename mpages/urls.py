from django.urls import path

from . import views

urlpatterns = [
    path("", views.PageListView.as_view(), name="page-list"),
    path(
        "children/<slug:parent_slug>/",
        views.PageListView.as_view(),
        name="page-list-filter",
    ),
    path("edit/<slug:slug>/", views.PageEditView.as_view(), name="page-edit"),
    path("<slug:slug>/", views.PageDetailView.as_view(), name="page-detail"),
]

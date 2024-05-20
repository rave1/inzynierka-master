from django.urls import path
from wca import views

urlpatterns = [
    path("", views.PersonsListView.as_view(), name="persons_list"),
    path("person/<str:pk>/", views.PersonDetailView.as_view(), name="person_detail"),
    path("competitions/", views.CompetitionListView.as_view(), name="competition_list"),
    path(
        "competitions/<str:pk>/",
        views.CompetitionDetailView.as_view(),
        name="competition_detail",
    ),
    path(
        "competitions/<str:competition_id>/results/",
        views.CompetitionResultsView.as_view(),
        name="competition_results",
    ),
]

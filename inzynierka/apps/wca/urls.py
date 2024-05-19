from django.urls import path
from wca import views

urlpatterns = [
    path("", views.PersonsListView.as_view(), name="persons_list"),
    path("person/<str:pk>/", views.PersonDetailView.as_view(), name="person_detail"),
]

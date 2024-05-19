# Create your views here.
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from wca.models import Persons, Competitions, Results


def home(request):
    return render(request, "persons.html")


class PersonsListView(ListView):
    model = Persons
    paginate_by = 10
    template_name = "persons.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Persons.objects.filter(name__icontains=query)
        else:
            return Persons.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class PersonDetailView(DetailView):
    model = Persons
    template_name = "person_detail.html"
    context_object_name = "person"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = self.object
        # Get results for this person
        results = Results.objects.filter(personid=person.id)
        competitions = Competitions.objects.filter(
            id__in=results.values_list("competitionid", flat=True)
        )
        # Create a dictionary mapping competitions to their results
        competition_results = {}
        for competition in competitions:
            competition_results[competition] = results.filter(
                competitionid=competition.id
            )
        context["competition_results"] = competition_results
        return context

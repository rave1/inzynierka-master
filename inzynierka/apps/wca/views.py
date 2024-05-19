# Create your views here.
from django.shortcuts import render
from django.views.generic.list import ListView
from wca.models import Persons


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

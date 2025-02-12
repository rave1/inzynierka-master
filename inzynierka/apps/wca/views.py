# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from wca.models import Persons, Competitions, Results
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from wca.forms import ProfileForm
from django.core.cache import cache


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


class CompetitionListView(ListView):
    model = Competitions
    template_name = "competition_list.html"
    context_object_name = "competitions"
    paginate_by = 10

    def get_queryset(self):
        queryset = Competitions.objects.all()

        # Filter by country
        country = self.request.GET.get("country")
        if country:
            queryset = queryset.filter(countryid=country)

        # Order by
        order_by = self.request.GET.get("order_by")
        order_dir = self.request.GET.get("order_dir")
        if order_by:
            if order_dir == "desc":
                order_by = f"-{order_by}"
            queryset = queryset.order_by(order_by)

        # Search
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["countries"] = Competitions.objects.values_list(
            "countryid", flat=True
        ).distinct()
        return context


class CompetitionDetailView(DetailView):
    model = Competitions
    template_name = "competition_detail.html"
    context_object_name = "competition"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition = self.object

        # Process WCA Delegate
        wcadelegate = competition.wcadelegate
        if wcadelegate:
            context["wcadelegates"] = self.parse_people_list(wcadelegate)
        else:
            context["wcadelegates"] = []

        # Process Organiser
        organiser = competition.organiser
        if organiser:
            context["organisers"] = self.parse_people_list(organiser)
        else:
            context["organisers"] = []

        # Process Event Specs
        event_specs = competition.eventspecs
        if event_specs:
            context["formatted_event_specs"] = self.format_event_specs(event_specs)
        else:
            context["formatted_event_specs"] = {}

        # Format Coordinates
        latitude = competition.latitude
        longitude = competition.longitude
        if latitude is not None and longitude is not None:
            context["formatted_coordinates"] = self.format_coordinates(
                latitude, longitude
            )
        else:
            context["formatted_coordinates"] = None

        return context

    def parse_people_list(self, people_list):
        people = []
        entries = people_list.strip("[]").split("][")
        for entry in entries:
            name_email = entry.strip("{}").split("}{")
            if len(name_email) == 2:
                person = {"name": name_email[0], "email": name_email[1]}
                people.append(person)
        return people

    def format_event_specs(self, event_specs):
        event_mapping = {
            "222": "2x2x2",
            "333": "3x3x3",
            "333oh": "3x3x3 One-hand",
            "444": "4x4x4",
            "555": "5x5x5",
            "666": "6x6x6",
            "777": "7x7x7",
            "clock": "Clock",
            "pyram": "Pyraminx",
            "skewb": "Skewb",
            "sq1": "Square-1",
        }
        events = event_specs.split()
        formatted_events = {event: event_mapping.get(event, event) for event in events}
        return formatted_events

    def format_coordinates(self, latitude, longitude):
        lat_str = str(latitude)
        lon_str = str(longitude)
        formatted_lat = f"{lat_str[:2]}.{lat_str[2:]}"
        formatted_lon = f"{lon_str[:2]}.{lon_str[2:]}"
        return f"{formatted_lat}, {formatted_lon}"


class CompetitionResultsView(ListView):
    model = Results
    template_name = "competition_results.html"
    context_object_name = "results"
    paginate_by = 20

    def get_queryset(self):
        competition_id = self.kwargs["competition_id"]
        queryset = Results.objects.filter(competitionid=competition_id)

        person = self.request.GET.get("person")
        if person:
            queryset = queryset.filter(personname__icontains=person)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition_id = self.kwargs["competition_id"]
        competition = get_object_or_404(Competitions, pk=competition_id)
        results = self.get_queryset()

        grouped_results = {}
        for result in results:
            person = result.personid
            if person not in grouped_results:
                grouped_results[person] = []
            grouped_results[person].append(result)

        context["competition"] = competition
        context["grouped_results"] = grouped_results
        return context


def format_time(centiseconds):
    minutes = centiseconds // 6000
    seconds = (centiseconds % 6000) // 100
    centis = centiseconds % 100
    return f"{minutes}:{seconds:02}.{centis:02}"


def results_data(request, competition_id):
    results = Results.objects.filter(competitionid=competition_id)

    event_data = cache.get("event_data", {})
    if event_data == {}:
        for result in results:
            event = result.eventid
            if event not in event_data:
                event_data[event] = {
                    "labels": [],
                    "best": [],
                    "average": [],
                    "raw_best": [],
                    "raw_average": [],
                }
            event_data[event]["labels"].append(result.personname)
            event_data[event]["best"].append(format_time(result.best))
            event_data[event]["average"].append(format_time(result.average))
            event_data[event]["raw_best"].append(result.best / 100.0)
            event_data[event]["raw_average"].append(result.average / 100.0)

        for event in event_data:
            event_data[event]["min_best"] = min(event_data[event]["raw_best"])
            event_data[event]["min_average"] = min(event_data[event]["raw_average"])
        cache.set("event_data", event_data, 15 * 60)

    return JsonResponse(event_data)


@login_required
def profile(request):
    if request.method == "POST":
        # user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        # if user_form.is_valid():
        #     user_form.save()
        #     return redirect("profile")
        if profile_form.is_valid():
            profile_form.save()
            return redirect("profile")
    else:
        # user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    # Get results based on WCA ID
    if request.user.profile.wca_id:
        results = Results.objects.filter(personid=request.user.profile.wca_id).order_by(
            "eventid", "best"
        )
    else:
        results = []

    for result in results:
        result.formatted_best = format_time(result.best)
        result.formatted_average = format_time(result.average)

    return render(
        request,
        "profile.html",
        {
            "profile_form": profile_form,
            "results": results,
        },
    )

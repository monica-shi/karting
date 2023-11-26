
# Create your views here.

from .models import Chassis, Engine, Session
from django.shortcuts import render
from django.views import generic


def index(request):
    """View function for home page of site."""

    num_chassis = Chassis.objects.count()
    num_engines = Engine.objects.count()
    num_sessions = Session.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_chassis': num_chassis,
        'num_engines': num_engines,
        'num_sessions': num_sessions,
    }

    return render(request, 'index.html', context=context)


class ChassisListView(generic.ListView):
    model = Chassis
    context_object_name = 'chassis_list'
    paginate_by = 10


class ChassisDetailView(generic.DetailView):
    model = Chassis


class EngineListView(generic.ListView):
    model = Engine
    context_object_name = 'engine_list'
    paginate_by = 10


class EngineDetailView(generic.DetailView):
    model = Engine


class SessionListView(generic.ListView):
    model = Session
    context_object_name = 'session_list'
    paginate_by = 10


class SessionDetailView(generic.DetailView):
    model = Session


# Create your views here.

from .models import Chassis, Engine, Session
from django.shortcuts import render
from django.views import generic

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import SessionForm


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
        'num_visits': num_visits,
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


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def create_session(request):
    """View function for renewing a specific BookInstance by librarian."""
    session_instance = Session()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SessionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            session_instance.due_back = form.cleaned_data['renewal_date']
            session_instance.date = form.cleaned_data['date']
            session_instance.time = form.cleaned_data['time']
            session_instance.track = form.cleaned_data['track']
            session_instance.chassis = form.cleaned_data['chassis']
            session_instance.engine = form.cleaned_data['engine']
            session_instance.save()

            # redirect to a new URL: (homepage)
            return HttpResponseRedirect(reverse('SessionListView'))

    # If this is a GET (or any other method) create the default form.
    else:
        current_date_time = datetime.datetime.now()
        form = SessionForm(initial={'date': current_date_time.date(), 'time':current_date_time.time()})

    context = {
        'form': form,
        'session_instance': session_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

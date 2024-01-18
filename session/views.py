
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
def create_session(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    session_instance = Session.objects.get(pk=pk)
    session_instance.pk = None

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




from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Chassis, Engine, Session
from django.contrib.auth.mixins import PermissionRequiredMixin


class ChassisCreate(PermissionRequiredMixin, CreateView):
    model = Chassis
    fields = ['brand', 'year', 'model', 'description']
    initial = {'year': datetime.datetime.now().year, 'brand': 'OTK'}
    permission_required = 'session.add_chassis'

class ChassisUpdate(PermissionRequiredMixin, UpdateView):
    model = Chassis
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'session.change_chassis'

class ChassisDelete(PermissionRequiredMixin, DeleteView):
    model = Chassis
    success_url = reverse_lazy('chassis')
    permission_required = 'session.delete_chassis'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("chassis-delete", kwargs={"pk": self.object.pk})
            )


class EngineCreate(PermissionRequiredMixin, CreateView):
    model = Engine
    fields = ['manufacturer', 'model', 'nickname', 'serial_num']
    # initial = {''}
    permission_required = 'session.add_engine'


class EngineUpdate(PermissionRequiredMixin, UpdateView):
    model = Engine
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'session.change_engine'


class EngineDelete(PermissionRequiredMixin, DeleteView):
    model = Engine
    success_url = reverse_lazy('engine')
    permission_required = 'session.delete_engine'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("engine-delete", kwargs={"pk": self.object.pk})
            )


class SessionCreate(PermissionRequiredMixin, CreateView):
    model = Session
    fields = '__all__'
    initial = {'date': datetime.date.today()}
    permission_required = 'session.add_session'


class SessionClone(PermissionRequiredMixin, CreateView):
    model = Session
    fields = '__all__'
    permission_required = 'session.add_session'

    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs['pk']
        old_session = Session.objects.get(pk=pk)
        initial['date'] = datetime.date.today()
        initial['session_time'] = datetime.datetime.now()
        initial['race'] = old_session.race
        initial['session_type'] = old_session.session_type
        initial['track'] = old_session.track
        initial['track_conditions'] = old_session.track_conditions
        initial['weather'] = old_session.weather
        initial['chassis'] = old_session.chassis
        initial['engine'] = old_session.engine
        initial['engine_driver_size'] = old_session.engine_driver_size
        initial['sprocket_size'] = old_session.sprocket_size
        initial['tire'] = old_session.tire
        initial['tire_type'] = old_session.tire_type
        initial['rim'] = old_session.rim
        initial['high_jetting'] = old_session.high_jetting
        initial['low_jetting'] = old_session.low_jetting
        initial['castor'] = old_session.castor
        initial['camber'] = old_session.camber
        initial['rear_axle_type'] = old_session.rear_axle_type
        initial['rear_width'] = old_session.rear_width
        return initial


class SessionUpdate(PermissionRequiredMixin, UpdateView):
    model = Session
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'session.change_session'


class SessionDelete(PermissionRequiredMixin, DeleteView):
    model = Chassis
    success_url = reverse_lazy('session')
    permission_required = 'session.delete_session'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("session-delete", kwargs={"pk": self.object.pk})
            )

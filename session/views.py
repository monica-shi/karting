# Create your views here.

import datetime

import django.forms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q

from .forms import SessionForm
from .models import Chassis, Engine, Session, Track


def index(request):
    """View function for home page of site."""

    num_chassis = Chassis.objects.filter(user=request.user.id).count()
    num_engines = Engine.objects.filter(user=request.user.id).count()
    num_sessions = Session.objects.filter(user=request.user.id).count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_chassis': num_chassis,
        'num_engines': num_engines,
        'num_sessions': num_sessions,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class UserFilteredListView(generic.ListView):
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user.id)


class UserFilteredDetailView(generic.DetailView):
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user.id)


class ChassisListView(UserFilteredListView):
    model = Chassis
    context_object_name = 'chassis_list'
    paginate_by = 50


class ChassisDetailView(UserFilteredDetailView):
    model = Chassis


class EngineListView(UserFilteredListView):
    model = Engine
    context_object_name = 'engine_list'
    paginate_by = 50


class EngineDetailView(UserFilteredDetailView):
    model = Engine


class SessionListView(UserFilteredListView):
    model = Session
    context_object_name = 'session_list'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).order_by('-date', '-session_time')


class SessionDetailView(UserFilteredDetailView):
    model = Session


class ChassisCreate(PermissionRequiredMixin, CreateView):
    model = Chassis
    fields = ['brand', 'year', 'model', 'description']
    initial = {'year': datetime.datetime.now().year, 'brand': 'OTK'}
    permission_required = 'session.add_chassis'

    def form_valid(self, form):
        chassis = form.save(commit=False)
        chassis.user = self.request.user
        return super().form_valid(form)


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

    def form_valid(self, form):
        engine = form.save(commit=False)
        engine.user = self.request.user
        return super().form_valid(form)


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


class TrackListView(generic.ListView):
    model = Track
    context_object_name = 'track_list'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(Q(created_by_id=self.request.user.id) | Q(created_by_id=1))


class TrackDetailView(generic.DetailView):
    model = Track

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(Q(created_by_id=self.request.user.id) | Q(created_by_id=1))


class SessionCreationView(CreateView):
    model = Session
    form_class = SessionForm

    def get_form_class(self):
        model_form = super().get_form_class()
        # Users can only see the tracks they added, or those added by user 'karting'
        model_form.base_fields['track'].limit_choices_to = Q(created_by=self.request.user) | Q(created_by_id=1)
        model_form.base_fields['chassis'].limit_choices_to = Q(user=self.request.user)
        model_form.base_fields['engine'].limit_choices_to = Q(user=self.request.user)

        if 'result_photo' not in model_form.base_fields:
            base_fields_with_file = {}
            for key in model_form.base_fields:
                if key == 'lap_time1':
                    base_fields_with_file['result_photo'] \
                        = django.forms.FileField(required=False,
                                                 help_text="Take a photo of your MyChron/UniPro dash "
                                                           "to auto fill the results")
                base_fields_with_file[key] = model_form.base_fields[key]
            model_form.base_fields = base_fields_with_file

        return model_form

    def form_valid(self, form):
        session = form.save(commit=False)
        session.user = self.request.user
        return super().form_valid(form)


class TrackCreate(PermissionRequiredMixin, CreateView):
    model = Track
    fields = ['name', 'country', 'website']
    permission_required = 'session.add_track'

    def form_valid(self, form):
        track = form.save(commit=False)
        track.created_by = self.request.user
        return super().form_valid(form)


class TrackUpdate(PermissionRequiredMixin, UpdateView):
    model = Track
    # Not recommended (potential security issue if more fields added)
    fields = ['name', 'country', 'website']
    permission_required = 'session.change_track'

    def form_valid(self, form):
        track = form.save(commit=False)
        if track.created_by != self.request.user:
            return HttpResponseBadRequest("You are not allowed to change a track created by another person")
        else:
            return super().form_valid(form)


class TrackDelete(PermissionRequiredMixin, DeleteView):
    model = Track
    success_url = reverse_lazy('track')
    permission_required = 'session.delete_track'

    def form_valid(self, form):
        try:
            if self.object.created_by != self.request.user:
                return HttpResponseBadRequest("You are not allowed to delete a track created by another person")
            else:
                self.object.delete()
                return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseServerError(
                'Server error: %s'.format(e)
            )


class SessionCreate(PermissionRequiredMixin, SessionCreationView):
    model = Session
    initial = {'date': datetime.date.today(), 'session_time': datetime.datetime.now()}
    permission_required = 'session.add_session'


class SessionClone(PermissionRequiredMixin, SessionCreationView):
    model = Session
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
        initial['temp'] = old_session.temp
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


class SessionUpdateView(UpdateView):
    model = Session
    form_class = SessionForm


class SessionUpdate(PermissionRequiredMixin, SessionUpdateView):
    model = Session
    # Not recommended (potential security issue if more fields added)
    permission_required = 'session.change_session'


class SessionDelete(PermissionRequiredMixin, DeleteView):
    model = Session
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


class SessionCompare(generic.TemplateView):
    template_name = 'session/session_compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_ids = self.request.GET.getlist('sessions')
        context['session_list'] = [Session.objects.get(pk=pk) for pk in session_ids]
        return context

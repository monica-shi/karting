# Create your views here.
import datetime
import io
import logging

import boto3
import django.forms
from PIL import Image
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q

from .forms import SessionForm
from .models import Chassis, Engine, Session, Track
from .open_ai import parse_gauge_img


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
                    help_text = ('Take a photo of your MyChron to auto fill the results. We currently only support '
                                 'MyChron 5 dash and UniPro. Scroll down and press the "Submit" button. This upload '
                                 'may take some time, please be patient.')
                    base_fields_with_file['gauge_type'] \
                        = django.forms.ChoiceField(
                            required=False, choices=(('MyChron5', 'MyChron5'), ('UniPro', 'UniPro')))
                    base_fields_with_file['result_photo'] \
                        = django.forms.ImageField(required=False,
                                                  help_text=help_text)
                base_fields_with_file[key] = model_form.base_fields[key]
            model_form.base_fields = base_fields_with_file

        return model_form

    @staticmethod
    def _parse_lap_time_str(lap_time_str):
        result_decimal = float(0)
        minunte_splits = lap_time_str.split(':')
        if len(minunte_splits) > 1:
            result_decimal += float(minunte_splits[0]) * 60
            result_decimal += float(minunte_splits[1])
        else:
            result_decimal += float(minunte_splits[0])
        return result_decimal

    def form_valid(self, form):
        session = form.save(commit=False)
        session.user = self.request.user

        result_img = self.request.FILES.get('result_photo')
        gauge_type = form.data['gauge_type']
        if result_img:
            img_buffer = self.get_image_buffer(result_img)
            try:
                s3 = boto3.client(
                    's3',
                )
                s3.put_object(Bucket='karting-test',
                              Key=f'{session.date}/{session.driver_name}/result_photo_{session.session_time}.jpg',
                              Body=img_buffer,
                              ContentType='image/jpeg',
                              )
            except Exception as e:
                logging.error(f'Error uploading photo to S3: {e}')

            result_dict = parse_gauge_img(img_buffer, gauge_type)
            if gauge_type == 'MyChron5':
                session.lap_time1 = self._parse_lap_time_str(result_dict['BEST LAPS'][0])
                session.lap_time2 = self._parse_lap_time_str(result_dict['BEST LAPS'][1])
                session.lap_time3 = self._parse_lap_time_str(result_dict['BEST LAPS'][2])
                session.rpm_max1 = int(result_dict['RPM'][0])
                session.rpm_max2 = int(result_dict['RPM'][2])
                session.rpm_max3 = int(result_dict['RPM'][4])
                session.rpm_min1 = int(result_dict['RPM'][1])
                session.rpm_min2 = int(result_dict['RPM'][3])
                session.rpm_min3 = int(result_dict['RPM'][5])
                session.speed_max1 = float(result_dict['MPH'][0])
                session.speed_max2 = float(result_dict['MPH'][2])
                session.speed_max3 = float(result_dict['MPH'][4])
                session.speed_min1 = float(result_dict['MPH'][1])
                session.speed_min2 = float(result_dict['MPH'][3])
                session.speed_min3 = float(result_dict['MPH'][5])
                session.egt_max1 = int(result_dict['EGT'][0])
                session.egt_max2 = int(result_dict['EGT'][2])
                session.egt_max3 = int(result_dict['EGT'][4])
                session.egt_min1 = int(result_dict['EGT'][1])
                session.egt_min2 = int(result_dict['EGT'][3])
                session.egt_min3 = int(result_dict['EGT'][5])
            else:  # else if gauge_type == 'UniPro':
                session.lap_time1 = self._parse_lap_time_str(result_dict['LAP TIME'][0])
                session.lap_time2 = self._parse_lap_time_str(result_dict['LAP TIME'][1])
                session.lap_time3 = self._parse_lap_time_str(result_dict['LAP TIME'][2])
                session.rpm_max1 = int(float(result_dict['RPM'][0]) * 1000)
                session.rpm_max2 = int(float(result_dict['RPM'][2]) * 1000)
                session.rpm_max3 = int(float(result_dict['RPM'][4]) * 1000)
                session.rpm_min1 = int(float(result_dict['RPM'][1]) * 1000)
                session.rpm_min2 = int(float(result_dict['RPM'][3]) * 1000)
                session.rpm_min3 = int(float(result_dict['RPM'][5]) * 1000)
                session.speed_max1 = float(result_dict['GPS SPEED'][0])
                session.speed_max2 = float(result_dict['GPS SPEED'][2])
                session.speed_max3 = float(result_dict['GPS SPEED'][4])
                session.speed_min1 = float(result_dict['GPS SPEED'][1])
                session.speed_min2 = float(result_dict['GPS SPEED'][3])
                session.speed_min3 = float(result_dict['GPS SPEED'][5])
                session.egt_max1 = int(result_dict['TEMP 1'][0])
                session.egt_max2 = int(result_dict['TEMP 1'][2])
                session.egt_max3 = int(result_dict['TEMP 1'][4])
                session.egt_min1 = int(result_dict['TEMP 1'][1])
                session.egt_min2 = int(result_dict['TEMP 1'][3])
                session.egt_min3 = int(result_dict['TEMP 1'][5])

        return super().form_valid(form)

    @staticmethod
    def get_image_buffer(img_file):
        with Image.open(img_file) as pil_img:
            # Rotate the image if it is in portrait mode
            if pil_img.height > pil_img.width:
                pil_img = pil_img.rotate(90, expand=True)

            img_bytes = io.BytesIO()
            pil_img.save(img_bytes, format='JPEG')
            return img_bytes.getvalue()

    def update_session_with_ocr_result(self, session, result_dict):
        session.lap_time1 = self._parse_lap_time_str(result_dict['BEST LAPS'][0])
        session.lap_time2 = self._parse_lap_time_str(result_dict['BEST LAPS'][1])
        session.lap_time3 = self._parse_lap_time_str(result_dict['BEST LAPS'][2])
        session.rpm_max1 = int(result_dict['RPM'][0])
        session.rpm_max2 = int(result_dict['RPM'][2])
        session.rpm_max3 = int(result_dict['RPM'][4])
        session.rpm_min1 = int(result_dict['RPM'][1])
        session.rpm_min2 = int(result_dict['RPM'][3])
        session.rpm_min3 = int(result_dict['RPM'][5])
        session.speed_max1 = float(result_dict['MPH'][0])
        session.speed_max2 = float(result_dict['MPH'][2])
        session.speed_max3 = float(result_dict['MPH'][4])
        session.speed_min1 = float(result_dict['MPH'][1])
        session.speed_min2 = float(result_dict['MPH'][3])
        session.speed_min3 = float(result_dict['MPH'][5])
        session.egt_max1 = int(result_dict['EGT'][0])
        session.egt_max2 = int(result_dict['EGT'][2])
        session.egt_max3 = int(result_dict['EGT'][4])
        session.egt_min1 = int(result_dict['EGT'][1])
        session.egt_min2 = int(result_dict['EGT'][3])
        session.egt_min3 = int(result_dict['EGT'][5])


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
        initial['driver_name'] = old_session.driver_name
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

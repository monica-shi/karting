from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chassis/', views.ChassisListView.as_view(), name='chassis'),
    path('chassis/<int:pk>', views.ChassisDetailView.as_view(), name='chassis-detail'),
    path('engine/', views.EngineListView.as_view(), name='engine'),
    path('engine/<int:pk>', views.EngineDetailView.as_view(), name='engine-detail'),
    path('session/', views.SessionListView.as_view(), name='session'),
    path('session/<int:pk>', views.SessionDetailView.as_view(), name='session-detail'),

    path('session/add/', views.create_session, name='add-session'),

]

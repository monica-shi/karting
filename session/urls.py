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

    path('chassis/create/', views.ChassisCreate.as_view(), name='chassis-create'),
    path('chassis/<int:pk>/update/', views.ChassisUpdate.as_view(), name='chassis-update'),
    path('chassis/<int:pk>/delete/', views.ChassisDelete.as_view(), name='chassis-delete'),


    path('engine/create/', views.EngineCreate.as_view(), name='engine-create'),
    path('engine/<int:pk>/update/', views.EngineUpdate.as_view(), name='engine-update'),
    path('engine/<int:pk>/delete/', views.EngineDelete.as_view(), name='engine-delete'),

    path('session/create/', views.SessionCreate.as_view(), name='session-create'),
    path('session/<int:pk>/update/', views.SessionUpdate.as_view(), name='session-update'),
    path('session/<int:pk>/delete/', views.SessionDelete.as_view(), name='session-delete'),

]

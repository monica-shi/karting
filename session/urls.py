from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chassis/', views.ChassisListView.as_view(), name='chassis'),
    path('chassis/<int:pk>', views.ChassisDetailView.as_view(), name='chassis-detail'),
    path('engine/', views.EngineListView.as_view(), name='engine'),
    path('engine/<int:pk>', views.EngineDetailView.as_view(), name='engine-detail'),
]

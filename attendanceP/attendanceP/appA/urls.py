from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('adminpage/', views.adminPage, name='adminpage'),
    path('take/<str:branch>', views.takeAttendance, name='takeAttendance'),
]
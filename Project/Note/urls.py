from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.identification, name='identification'),
    path('win/', views.win, name='win'),
]

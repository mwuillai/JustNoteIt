from django.urls import path
from django.urls import include

from . import views

app_name = "Note"
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.identification, name='identification'),
    path('notes/<slug:slug>', views.DetailNotesView.as_view(), name='detail'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard')
]
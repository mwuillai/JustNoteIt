from django.urls import path
from django.urls import include

from . import views

app_name = "Note"
urlpatterns = [
    path('', views.identification, name='identification'),
    path('notes/<slug:slug>', views.DetailNotesView.as_view(), name='detail'),
    path('edit-note/<slug:slug>', views.UpdateNoteView.as_view(), name='edit_note'),
    path('category/<slug:slug>', views.DetailCategoriesView.as_view(), name='category'),
    path('new-note/', views.CreateNoteView.as_view(), name='new_note'),
    path('new-category/', views.CreateCategoryView.as_view(), name='new_category'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('delete_note/<slug:slug>', views.DeleteNoteView.as_view(), name='delete_note'),
    path('delete_category/<slug:slug>', views.DeleteCategoryView.as_view(), name='delete_category'),
    path('logout/', views.logout_view, name='logout'),
    ]

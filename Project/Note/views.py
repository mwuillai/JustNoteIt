from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Category, Notes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.http import JsonResponse
from .forms import NotesForm, CategoryForm
from django.urls import reverse_lazy
from django.http import Http404

def add_categories_in_context(func):
    """
    Decorator to put on get_context method in a view class to update
    the context with categories. Categories are present in each view of
    the dashboard
    """
    def inner(self, *args, **kwargs):
        context = func(self, *args, **kwargs)
        current_user = self.request.user
        context.update({
            'categories': Category.objects.filter(user_id=current_user.id),
        })
        return context
    return inner

def identification(request):
    """
    Views identification, there is two form on this views
    the first is the native authentication django form and the
    second one is the userCreationForm. in the post response
    the difference between those two form is made with the input button.
    TODO manage error message
    """
    if request.method == "POST":
        if 'Authentication' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("Note:dashboard")
            
            return redirect('Note:identification')
        elif 'Sign up' in request.POST:
            form = UserCreationForm(request.POST)
            try:
                form.save()
            except ValueError:
                return redirect('Note:identification')
            return redirect('Note:dashboard')
    else:
        if request.user.is_authenticated:
            return redirect("Note:dashboard")
        else :
            sign_up_form = UserCreationForm()
            auth_form = AuthenticationForm()
            return render(request, 'Note/identification.html', {
                'auth':auth_form,
                'sign_up':sign_up_form
            })

def logout_view(request):
    """
    Simple logout view
    """
    logout(request)
    return redirect('Note:identification')


class Dashboard(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call notes."""
    model = Notes
    paginate_by = 15
    context_object_name = "notes"
    template_name = "Note/dashboard.html"

    @add_categories_in_context
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, **kwargs):
        current_user = self.request.user
        return Notes.objects.filter(user_id=current_user.id)


class DetailNotesView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual Notes."""
    model = Notes
    context_object_name = "note"
    template_name = "Note/detail.html"

    @add_categories_in_context
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class DetailCategoriesView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation for filter notes of an individual category."""
    model = Category
    context_object_name = "main_category"
    template_name = "Note/category.html"

    @add_categories_in_context
    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'notes': Notes.objects.filter(user_id=current_user.id, category_id=self.get_object().pk),
        })
        return context

"""
TODO use this tutorial https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html
for wirting two ajax method, one to add on the go a new category and another to get the category list
In this I will be able to refresh categoryh list of a form without refresh the whole page
"""


class CreateNoteView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new notes.
    TODO add category selection, manage filter of category selection on current user
    """
    model = Notes
    message = "Your note has been created."
    form_class = NotesForm
    template_name = 'Note/add_note.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)
    
    @add_categories_in_context
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('Note:dashboard')


class UpdateNoteView(LoginRequiredMixin, UpdateView):
    model = Notes
    form_class = NotesForm
    template_name = "Note/add_note.html"

    @add_categories_in_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_success_url(self):
        return reverse('Note:dashboard')


class DeleteNoteView(LoginRequiredMixin, DeleteView):
    """
    Basic view to delete a note. We have to check if the delete note is the owner of the note
    """
    model = Notes
    success_url = reverse_lazy('Note:dashboard')

    def get_object(self, queryset=None):
        object = super(DeleteNoteView, self).get_object()
        if not object.user_id == self.request.user:
            raise Http404
        return object


class CreateCategoryView(LoginRequiredMixin, CreateView):
    """
    Basic CreateView implementation to create new Category.
    """
    model = Category
    message = "Your note has been created."
    form_class = CategoryForm
    template_name = 'Note/add_category.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)
    
    @add_categories_in_context
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('Note:dashboard')


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    """
    Basic view to delete a category. We have to check if the delete note is the owner of the note
    """
    model = Category
    success_url = reverse_lazy('Note:dashboard')

    def get_object(self, queryset=None):
        object = super(DeleteCategoryView, self).get_object()
        if not object.user_id == self.request.user:
            raise Http404
        return object
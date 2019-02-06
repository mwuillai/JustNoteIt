from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Category, Notes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse
from .forms import NotesForm

def identification(request):
    """
    Views identification, there is two form on this views
    the first is the native authentication django form and the
    second one is the userCreationForm. in the post response
    the difference between those two form is made with the input button.

    STILL TO DO : Manage the possibility of a login user from a previous session
    who will directly reach the dashboard view
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
        sign_up_form = UserCreationForm()
        auth_form = AuthenticationForm()
        return render(request, 'Note/identification.html', {
            'auth':auth_form,
            'sign_up':sign_up_form
        })


class Dashboard(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call notes."""
    model = Notes
    paginate_by = 15
    context_object_name = "notes"
    template_name = "Note/dashboard.html"

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'categories': Category.objects.filter(user_id=current_user.id),
        })
        return context

    def get_queryset(self, **kwargs):
        current_user = self.request.user
        return Notes.objects.filter(user_id=current_user.id)


class DetailNotesView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual Notes."""
    model = Notes
    context_object_name = "notes"
    template_name = "Note/detail.html"

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'categories': Category.objects.filter(user_id=current_user.id),
        })
        return context


class DetailCategoriesView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation for filter notes of an individual category."""
    model = Category
    context_object_name = "categories"
    template_name = "Note/category.html"

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'notes': Notes.objects.filter(user_id=current_user.id, category__slug=self.get_object().slug),
        })
        return context

"""
TODO use this tutorial https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html
for wirting two ajax method, one to add on the go a new category and another to get the category list
In this I will be able to refresh categoryh list of a form without refresh the whole page
"""


class CreateNoteView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new notes."""
    model = Notes
    # message = _("Your note has been created.")
    form_class = NotesForm
    template_name = 'Note/add_note.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # messages.success(self.request, self.message)
        return reverse('Note:dashboard')

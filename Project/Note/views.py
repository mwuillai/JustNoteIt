from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login


def identification(request):
    """
    Views identification, there is two form on this views
    the first is the native authentication django form and the 
    second one is the userCreationForm. in the post response
    the difference between those two form is made with the input button.
    """
    if request.method == "POST":
        if 'Authentication' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("win")
        elif 'Sign up' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('win')
    else:
        sign_up_form = UserCreationForm()
        auth_form = AuthenticationForm()
        return render(request, 'Note/identification.html',{
            'auth':auth_form,
            'sign_up':sign_up_form
        })

def win(request):
    return render(request, 'Note/win.html')

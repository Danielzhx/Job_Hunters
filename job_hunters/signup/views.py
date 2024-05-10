from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import IndividualForm, SignupForm


# Create your views here.
def signup_type(request):
    """First step in new account registration.
    
    Allows the user to choose whether they want to create a 
    company or individual account.
    """
    template_name = "signup/index.html"
    return render(request, template_name, None)


def reg_individual(request):
    """Second step in new account registration for individuals.
    
    Takes in only the required info to create a new user. Project specific 
    info is handled in the next step.
    """
    template_name = "signup/reg_individual.html"
    if request.method == 'POST':
        print('Post method received')
        signup = SignupForm(data=request.POST)
        print('Form created')
        print(f"is signup valid? {signup.is_valid()}")
        if signup.is_valid():
            signup.save()
            return redirect("jobs:index")
        else:
            return render(request, template_name, {'errors': signup.errors})
    else:
        return render(request, template_name, {})


def register_profile(request):
    """Third step in new account registration for individuals.
    
    Gets project specific info which is added to both the user object and 
    its associated individual object.
    """
    template_name = "signup/register_profile.html"
    if request.method == 'POST':
        profile_form = IndividualForm(data=request.POST, user=request.user)

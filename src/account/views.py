from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import StudentSignUpForm


def signup(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.save()
            user.refresh_from_db()
            user.profile.dob = form.cleaned_data.get('dob')
            user.profile.address = form.cleaned_data.get('address')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = user.username, password=raw_password)
            login(request, user)
            return redirect('/book')
    else:
        form = StudentSignUpForm()
    return render(request, 'account/signup.html', {'form': form})

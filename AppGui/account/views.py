from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import AccountProfileForms, AccountPasswordForms


@login_required(login_url='/management/')
def profile(request):
    if request.method == 'POST':
        forms = AccountProfileForms(request.POST)
        # print(request.POST)
        if forms.is_valid():
            user_obj = User.objects.get(username=request.user)
            datas = forms.cleaned_data
            first_name = datas["FirstName"]
            last_name = datas["LastName"]
            email = datas["Email"]
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = email
            user_obj.save()

        return render(request, 'management/account/profile.html', {'form': forms})
    else:
        user_obj = User.objects.get(username=request.user)
        print(user_obj.username)
        data = {
            "FirstName": user_obj.first_name,
            "LastName": user_obj.last_name,
            "Email": user_obj.email
        }
        forms = AccountProfileForms(initial=data)
        forms_password = AccountPasswordForms(initial=None)
        return render(request, 'management/account/profile.html', {'form': forms, 'form_password': forms_password})


@login_required(login_url='/management/')
def password(request):
    if request.method == 'POST':
        forms = AccountPasswordForms(request.POST)
        # print(request.POST)
        if forms.is_valid():
            user_obj = User.objects.get(username=request.user)
            datas = forms.cleaned_data
            user_password = datas["Password"]
            user_repassword = datas["RePassword"]

            if user_password == user_repassword:
                print(user_password)
                user_obj.set_password(user_password)
                user_obj.save()

    return redirect('AccountProfile')

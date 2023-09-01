from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import LoginForm, UserRegistrationForm, \
                   UserEditForm, ProfileEditForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse
import folium
import requests
import json
import socket
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'vacina/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'core/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {'section': 'dashboard'})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'core/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})



def index(request):

    url = 'https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/sp'
    headers = {}
    response = requests.request('GET', url, headers=headers)
    dados_covid = json.loads(response.content)
    dados_covid['datetime'] = pd.to_datetime(dados_covid['datetime'])

    url2 = 'https://covid19-brazil-api.now.sh/api/report/v1/brazil'
    headers = {}
    response2 = requests.request('GET', url2, headers=headers)
    dados_covid2 = json.loads(response2.content)
    print(dados_covid2)
    print(dados_covid)

    return render(request, 'core/index.html', {'dados_covid': dados_covid,'dados_covid2': dados_covid2})

def Mostra_Mapa(request):
    l1 = "-23.547169"
    l2 = "-46.636719"
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    print(f"Hostname: {hostname}")
    print(f"IP Local: {ip_address}")
    ip_address2="187.94.185.34"
    print(f"IP Address: {ip_address2}")
    ip = requests.get('https://api.ipify.org/')
    response = requests.post(f"http://ip-api.com/json/{ip_address}").json()
    print(response)
    if (response['status'] !='fail'):
        l1 = response['lat']
        l2 = response['lon']


    m = folium.Map(location=[l1, l2], zoom_start=14, control_scale=True, width=1090, height=450)
    folium.Marker(location=[float(l1), float(l2)]).add_to(m)
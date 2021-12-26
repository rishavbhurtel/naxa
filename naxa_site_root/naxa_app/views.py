# from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, logout
from naxa_app.forms import UserForm, ProfileForm
from django.db import transaction
from django.core.paginator import Paginator
from naxa_app.models import Home, Office, Line
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, request
from django.core import exceptions


def home(request):
    return render(request, 'naxa_app/home.html')


@transaction.atomic
def signup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        print(user_form, profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            # Reload the profile form with the profile instance
            profile_form = ProfileForm(request.POST, instance=user.profile)
            # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.full_clean()
            profile_form.save()  # save the form
            home = profile_form.cleaned_data.get('home_location')
            office = profile_form.cleaned_data.get('office_location')
            home_lat, home_long = (home.split(
                ",")[0]).strip(), (home.split(",")[1]).strip()
            office_lat, office_long = (office.split(
                ",")[0]).strip(), (office.split(",")[1]).strip()
            location = Home(user_id=user.id, longitude=float(home_lat),
                            latitude=float(home_long))
            location.save()
            location = Office(
                user_id=user.id, longitude=float(office_lat), latitude=float(office_long))
            location.save()
            intermediates(user.id, [home_lat,home_long], [office_lat,office_long])
            auth.login(request, user)
            return redirect('home')
        else:
            error = user_form.errors if user_form.errors else profile_form.errors
            return render(request, 'naxa_app/login.html', {'error': error})
    user_form = UserForm()
    profile_form = ProfileForm()
    return render(request, 'naxa_app/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'naxa_app/login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'naxa_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def list_users(request):
    users_list = User.objects.only(
        "first_name", "last_name", "email"
    ).select_related('profile')
    paginator = Paginator(users_list, 3)  # Show 3 per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'naxa_app/user_list.html', context)


@login_required(login_url='/')
def geo_json(request):
    geo = Line.objects.get(user_id=request.user.id)
    try:
        response = JsonResponse({"type": "Feature",
                                "geometry": {
                                    "type": "Line",
                                    "coordinates": geo.line_vector
                                }
        })
    except exceptions.ObjectDoesNotExist:
        response = JsonResponse({"error": "data not available"})
    return response


@login_required(login_url='/')
def nearby(request, coordinate=None): # work remaining for this function.
    if request.method == 'POST':
        coordinate = request.POST['coordinate']
        coordinate = coordinate.split(",")
        lat, long = float(coordinate[0].strip()), float(coordinate[1].strip())
        # Spherical Law of Cosines
        params = {"lat": lat, "long": long}
        query = '''SELECT a.latitude, a.longitude FROM naxa_app_home as a
            WHERE(
                acos(sin(a.latitude * 0.0175) * sin(%(lat)s * 0.0175)
                     + cos(a.latitude * 0.0175) * cos(%(lat)s * 0.0175) *
                     cos((%(long)s * 0.0175) - (a.longitude * 0.0175))
                     ) * 6371'''
        locations = Home.objects.raw(query, translations=params)
        loc_list = [location for location in locations]
        return JsonResponse({"coordinate": loc_list})
    else:
        return render(request, 'naxa_app/nearby.html')


def intermediates(id, p1, p2, nb_points=3):  # just for test sake
    '''Return a list of nb_points equally spaced points
    between p1 and p2'''
    # If we have 8 intermediate points, we have 8+1=9 spaces
    # between p1 and p2
    x_spacing = (float(p2[0]) - float(p1[0])) / (nb_points + 1)
    y_spacing = (float(p2[1]) - float(p1[1])) / (nb_points + 1)

    lines_list = [[float(p1[0]) + i * x_spacing, float(p1[1]) + i * y_spacing]
                  for i in range(1, nb_points+1)]
    line = Line(user_id=id, line_vector=lines_list)
    line.save()

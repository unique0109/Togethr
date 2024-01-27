from django.shortcuts import render, redirect

from . forms import CreateUserForm,LoginForm

from django.contrib.auth.decorators import login_required
from .models import Data
from .models import SearchHist
# authentication models nd function
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup

def scrape_gadget_info(search_query):
    print("called")
    url = f'https://www.gadgets360.com/search?searchtext={search_query}'
    
    try:
        response = requests.get(url)
        # print(response)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        if response.status_code == 200:
            return response.text
            # return response
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
    
    return None



def homepage(request):

    return render(request,'backend/home.html')


def result(request, pk):

    curr_username = request.user.username
    res = SearchHist.objects.get(username=curr_username, id = pk)
    context = {
        'Result':res
    }
    
    return render(request, 'backend/result.html', context=context)


def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("my-login")
        

    context = {'registerform':form}

    return render(request,'backend/register.html',context=context)




def my_login(request):

    form = LoginForm()

    if request.method == 'POST':


        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'loginform':form}

    return render(request,'backend/my-login.html',context=context)

def user_logout(request):

    auth.logout(request)

    return redirect("")

@login_required(login_url="my-login")


def dashboard(request):
    curr_username = request.user.username
    if 'q' in request.GET:
        q = request.GET['q']
        # print(q)
        search_query=q
        gadget_info = scrape_gadget_info(search_query)
        # print("here type is",gadget_info)
        # type(gadget_info)
        if gadget_info is None:
            gadget_info = "No Result available"
        # gadget_info = "result"
        search = SearchHist(username=curr_username,searchTitle=q,searchRes=gadget_info)
        search.save()

    
    data = SearchHist.objects.filter(username=curr_username).order_by('-id')
    context={
        'Data':data
    }
    return render(request,'backend/dashboard.html',context=context)






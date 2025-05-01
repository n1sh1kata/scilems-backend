from django.shortcuts import render, redirect
from django.contrib.auth import logout
import requests

API_BASE_URL = "http://localhost:8000/api/auth/"  # Update with your backend URL

def register_view(request):
    if request.method == 'POST':
        data = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'password2': request.POST['password2'],
        }
        response = requests.post(f"{API_BASE_URL}register/", data=data)
        if response.status_code == 201:
            return redirect('login')
        else:
            # Pass detailed error messages to the template
            errors = response.json()
            return render(request, 'pages/register.html', {'errors': errors, 'form_data': data})
    return render(request, 'pages/register.html')


def login_view(request):
    token = request.session.get('access_token')
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{API_BASE_URL}protected/", headers=headers)
        if response.status_code == 200:
            return redirect('protected')  # Redirect to the protected page if the token is valid
    
    if request.method == 'POST':
        data = {
            'username': request.POST['username'],
            'password': request.POST['password'],
        }
        response = requests.post(f"{API_BASE_URL}login/", data=data)
        if response.status_code == 200:
            request.session['access_token'] = response.json().get('access')
            return redirect('protected')
        else:
            errors = response.json()
            return render(request, 'pages/login.html', {'errors': errors, 'form_data': data})
    return render(request, 'pages/login.html')



def protected_view(request):
    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{API_BASE_URL}protected/", headers=headers)
    if response.status_code == 200:
        return render(request, 'pages/protected.html', {'message': response.json().get('message')})
    else:
        return redirect('login')
    

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()  # Clear session data
        return redirect('login')
    
def index_view(request):
    return render(request, 'pages/index.html')
from django.shortcuts import render


from .models import StudentProfiles
from rest_framework import viewsets
from .serializers import StudentSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentProfiles.objects.all()
    serializer_class = StudentSerializer

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirmpassword = request.POST.get('confirmpassword', '')
        
        if not all([username, email, password, confirmpassword]):
            return render(request, 'user_register.html', {'error': 'All fields are required'})
        
        if password == confirmpassword:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return render(request, 'user_login.html')
        else:
            return render(request, 'user_register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'user_register.html')
    
    
def dashboard(request):
    return render(request, 'dashboard.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'user_login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'user_login.html')
    
    
    
def home(request):
    return render(request, 'home.html')



def faculty(request):
    return render(request, 'dashboard.html')



def faculty_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        if password == cpassword:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return render(request, 'faculty.login.html')
        else:
            return render(request, 'faculty.register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'faculty.register.html')
    
    
def faculty_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'dashboard.html')
        else:
            return render(request, 'faculty.login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'faculty.login.html')
    
    
def profile(request):
    return render(request, 'student_profile.html')


def logout(request):
    logout(request)
    return render(request, 'user_login.html')


def faculty_home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'faculty_home.html')
        else:
            return render(request, 'faculty.login.html', {'error': 'Invalid username or password'})
    return render(request, 'faculty_home.html')


def faculty_profile(request):
    return render(request, 'faculty_profile.html')
    
    
def list_students(request):
    students = StudentProfiles.objects.all()
    return render(request, 'student_list.html', {'students': students})
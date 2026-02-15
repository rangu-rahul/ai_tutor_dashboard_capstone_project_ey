from django.shortcuts import render
from django.conf import settings


from .models import StudentProfiles, Course, Enrollment
from rest_framework import viewsets
from .serializers import StudentSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Q
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
            return render(request, 's_home.html')
        else:
            return render(request, 'user_login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'user_login.html')
    
    
    
def s_home(request):
    return render(request, 's_home.html')



def faculty(request):
    return render(request, 'dashboard.html')



def faculty_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirmpassword')
        
        if not all([username, email, password, cpassword]):
             return render(request, 'faculty.register.html', {'error': 'All fields are required'})
        
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
            return render(request, 'faculty_home.html')
        else:
            return render(request, 'faculty.login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'faculty.login.html')
    
    
def s_profile(request):
    return render(request, 's_profile.html')


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

def faculty_attendance(request):
    return render(request, 'faculty_attendence.html')

def faculty_assignments(request):
    return render(request, 'faculty_assignments.html')

def faculty_study_materials(request):
    return render(request, 'faculty_study_materials.html')
    
    
def list_students(request):
    students = StudentProfiles.objects.all()
    return render(request, 'student_list.html', {'students': students})



import json
import urllib.error
import urllib.request

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

class ChatbotInitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "status": "success",
            "message": "AI Tutor initialized and ready to help you!"
        })


class GeminiChatAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = (request.data.get('message') or '').strip()
        if not message:
            return Response(
                {"error": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return Response(
                {"error": "Server missing GEMINI_API_KEY."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-pro:generateContent?key="
            f"{api_key}"
        )
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": message}
                    ]
                }
            ]
        }
        request_data = json.dumps(payload).encode("utf-8")
        api_request = urllib.request.Request(
            url,
            data=request_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(api_request, timeout=20) as response:
                body = response.read().decode("utf-8")
            data = json.loads(body)
        except urllib.error.HTTPError as exc:
            error_body = ""
            try:
                error_body = exc.read().decode("utf-8")
            except Exception:
                error_body = ""
            return Response(
                {"error": "Gemini API error.", "details": error_body},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except Exception:
            return Response(
                {"error": "Gemini request failed."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        reply = ""
        try:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            reply = ""

        if not reply:
            return Response(
                {"error": "Empty response from Gemini."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({"reply": reply})


def s_courses(request):
    """Display all courses with optional search functionality"""
    search_query = request.GET.get('search', '')
    
    if search_query:
        courses = Course.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(instructor__icontains=search_query)
        )
    else:
        courses = Course.objects.all()
    
    # Get user's enrollments if authenticated
    user_enrollments = []
    if request.user.is_authenticated:
        user_enrollments = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
    
    context = {
        'courses': courses,
        'search_query': search_query,
        'user_enrollments': list(user_enrollments)
    }
    return render(request, 's_courses.html', context)


def s_course_detail(request, course_id):
    """Display individual course details"""
    try:
        course = Course.objects.get(id=course_id)
        enrollment = None
        
        if request.user.is_authenticated:
            try:
                enrollment = Enrollment.objects.get(student=request.user, course=course)
            except Enrollment.DoesNotExist:
                pass
        
        context = {
            'course': course,
            'enrollment': enrollment
        }
        return render(request, 's_course_detail.html', context)
    except Course.DoesNotExist:
        return render(request, 's_courses.html', {'error': 'Course not found'})


def logout(request):
    logout(request)
    return render(request, 'dashboard.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os, json

@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel("models/gemini-flash-latest")


        data = json.loads(request.body)
        user_msg = data.get("message", "")

        response = model.generate_content(user_msg)

        return JsonResponse({"reply": response.text})

    except Exception as e:
        print("❌ ERROR:", e)
        return JsonResponse({"error": str(e)}, status=500)


def s_grades(request):
    """Display student grades"""
    return render(request, 's_grades.html')

def s_assignments(request):
    """Display student assignments"""
    return render(request, 's_assignments.html')

def s_attendance(request):
    """Display student attendance"""
    return render(request, 's_attendence.html')

def s_study_materials(request):
    """Display study materials"""
    return render(request, 's_study_materials.html')

def s_upload_projects(request):
    """Display project upload page"""
    return render(request, 's_upload_projects.html')

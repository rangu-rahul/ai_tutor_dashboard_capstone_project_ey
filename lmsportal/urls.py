"""
URL configuration for lmsportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include


from smartaidashboard.views import (
    dashboard, user_register, user_login, s_home, faculty, faculty_register, faculty_login,
    StudentViewSet, s_profile, logout, faculty_home, faculty_profile, list_students,
    ChatbotInitAPIView, s_courses, s_course_detail, GeminiChatAPIView,
    s_grades, s_assignments, s_attendance, s_study_materials, s_upload_projects
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',dashboard,name = 'dashboard'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('login/s_home',s_home,name = 's_home'),
    path('faculty/',faculty,name = 'faculty'),
    path('faculty/register/', faculty_register, name='faculty_register'),
    path('faculty/register/login/', faculty_login, name='faculty_login'),
    path('api/', include(router.urls)),
    path('login/s_home/s_profile/', s_profile, name = 's_profile'),
    path('logout/', logout, name='logout'),
    path('login/faculty/home', faculty_home, name='faculty_home'),
    path('login/faculty/profile', faculty_profile, name = "faculty_profile"),
    path('login/faculty/list_students', list_students, name = "list_students"),
    path('init/', ChatbotInitAPIView.as_view(), name='chatbot_init'),
    path('api/gemini/', GeminiChatAPIView.as_view(), name='gemini_chat'),
    path('courses/', s_courses, name='s_courses'),
    path('courses/<int:course_id>/', s_course_detail, name='s_course_detail'),
    path('',logout, name = 'logout'),
    path("", include("smartaidashboard.urls")),
    # Student Pages
    path('login/s_home/s_grades/', s_grades, name = 's_grades'),
    path('login/s_home/s_assignments/', s_assignments, name = 's_assignments'),
    path('login/s_home/s_attendance/', s_attendance, name = 's_attendance'),
    path('login/s_home/s_study_materials/', s_study_materials, name = 's_study_materials'),
    path('login/s_home/s_upload_projects/', s_upload_projects, name = 's_upload_projects'),
]
